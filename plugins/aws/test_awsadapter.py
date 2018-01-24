"""
Test AWS Adapter.
"""
import logging
import os
from libcloud.compute.base import NodeImage, Node
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

# logging config
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# pytest config
pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = '.'

TEST_AMI_ID = 'ami-c24ef5bb'
TEST_NODE_NAME = 'test_node'
TEST_NODE_SIZE = 't2.micro'

class TestAwsAdapter:

    def test_list_ami(self, awsadapter):
        """
        Should return list of amis owned by user.
        """
        amis = awsadapter.list_amis()
        assert amis is not None

    def test_get_ami_by_id(self,awsadapter):
        """
        should return NodeImage object
        corresponding to AMI.
        """
        ami = awsadapter.get_ami_by_id(TEST_AMI_ID)
        assert ami is not None
        assert isinstance(ami, NodeImage)

    def test_list_instances(self, driver, awsadapter):
        """
        should return list of created aws instances
        """
        actual = driver.list_nodes()
        expected = awsadapter.list_instances()
        assert len(actual) == len(expected)

    def test_get_size_by_id(self, driver, awsadapter):
        return NotImplementedError


    def test_create_node(self, driver, awsadapter):

        before = self._get_running_nodes(driver)
        logger.debug("before: %d nodes" % len(before))

        try:
            created = awsadapter.create_node(
                name=TEST_NODE_NAME,
                img=TEST_AMI_ID,
                size=TEST_NODE_SIZE)
        finally:
            self._teardown(driver)

        after = self._get_running_nodes(driver)
        logger.debug("after: %d nodes" % len(after))

        if len(before) == 0:
            assert isinstance(created, Node)
            assert len(after) == len(before) + 1
        else:
            assert created is None



    def test_destroy_node(self, driver, awsadapter):
        # TODO
        return NotImplementedError

    def _get_running_nodes(self, driver):
        nodes = driver.list_nodes()
        return [n for n in nodes if n.state not in ['shutting-down','terminated']]

    def _teardown(self, driver):
        """
        Destroy all test nodes.
        """
        nodes = driver.list_nodes()
        logger.debug("TEARDOWN ALL NODES")
        for n in nodes:
            if n.name == TEST_NODE_NAME:
                driver.destroy_node(n)
