from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeImage
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AwsAdapter:

    def _validate(self,config):
        """
        Validate Config dictionary
        """
        if not config:
            raise RuntimeError("AWS Config empty")
        keys = ['access_id', 'secret_key', 'account_id', 'region']
        missing_keys = [key for key in keys if key not in config]
        if missing_keys:
            raise RuntimeError('AWS Config missing: "{}"'.format(missing_keys))

    def __init__(self, config):
        """
        Constructor, initializes libcloud.
        Creates-
        self._account_id
        self._driver
        """
        self._validate(config)
        """ init libcloud driver"""
        logger.debug("initializing libcloud EC2 driver")
        access_id = config['access_id']
        secret_key = config['secret_key']
        self.account_id = config['account_id']
        region = config['region']
        cls = get_driver(Provider.EC2)
        self._driver = cls(access_id, secret_key, region=region)

    def list_amis(self):
        """
        lists AWS AMIs owned by user.
        """
        images = self._driver.list_images(ex_owner=self.account_id)
        return images

    def get_ami_by_id(self, image_id):
        """
        given the image ID e.g. 'ami-12345' return the Image object.
        """
        images = self._driver.list_images(ex_owner=self.account_id)
        image = [i for i in images if i.id == image_id][0]
        return image

    def get_size_by_id(self, size_id):
        """
        get size object corresponding to a size_id string e.g 't2.micro'
        """
        sizes = self._driver.list_sizes()
        size = [i for i in sizes if i.id == size_id][0]
        return size

    def list_instances(self):
        """
        List all instances regardless of state, and return array,
        """
        nodes = self._driver.list_nodes()
        return [[n.name, n.state, n.public_ips] for n in nodes]

    def _get_running_node(self, node_name):
        """
        Get a running node object that matches a name.
        """
        nodes = self._driver.list_nodes()
        node = [i for i in nodes if (i.name == node_name and i.state != 'terminated')]
        return (len(node) > 0 and node or None)

    def _create_needed(self, node_name):
        if self._get_running_node(node_name) is not None:
            return False
        else:
            return True

    def _destroy_needed(self, node_name):
        if self._get_running_node(node_name) is None:
            return False
        else:
            return True

    def create_node(self, name, img, size):
        """
        Creates instance from AMI if needed.
        If instance matching the provided name already exists, no action.
        Returns a Node object corresponding to the created instance, 
        or None if instance was not created.
        """
        if self._create_needed(name):
            node = self._driver.create_node(
                name=name,
                image=self.get_ami_by_id(img),
                size=self.get_size_by_id(size))
            self._driver.wait_until_running([node])
            return node
        else:
            logger.debug("node %s already created, no action" % name)
            return None

    def _destroy_node(self,name):
        if self._destroy_needed(name):
            logger.debug("destroy node")
        else:
            logger.debug("node not found, no destroy")
