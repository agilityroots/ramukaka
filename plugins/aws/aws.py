from errbot import BotPlugin, botcmd
from optparse import OptionParser

from libcloud.compute.types import Provider, NodeState
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeImage
from libcloud.compute.drivers.ec2 import EC2SubnetAssociation
import os
import time
import logging
logging.basicConfig(level=logging.DEBUG)

class Aws(BotPlugin):

    def _startProgress(self,msg):
        if self._bot.mode == "slack":
            self._bot.add_reaction(msg, "hourglass")

    def _stopProgress(self,msg):
        if self._bot.mode == "slack":
            self._bot.remove_reaction(msg, "hourglass")


    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'access_id': os.environ['ERRBOT_AWS_ACCESS_KEY'],
            'secret_key': os.environ['ERRBOT_AWS_SECRET_KEY'],
            'account_id': os.environ['ERRBOT_AWS_ACCOUNT_ID'],
            'region': os.environ['ERRBOT_AWS_DEFAULT_REGION'],
            'keypair': os.environ['ERRBOT_AWS_KEYPAIR_NAME'],
            'datacenter': Provider.EC2
        }
        return config

    def _connect(self):
        """ connection to aws """
        access_id = self.config['access_id']
        secret_key = self.config['secret_key']
        datacenter = self.config['datacenter']
        account_id = self.config['account_id']
        region = self.config['region']
        cls = get_driver(datacenter)
        driver = cls(access_id, secret_key, region=region)
        return driver

    def _list_amis(self,msg):
        """
        Private method, lists AWS AMIs.
        """
        self._startProgress(msg)
        driver = self._connect()
        account_id = self.config['account_id']
        images = driver.list_images(ex_owner=account_id)
        for img in images:
            self.log.debug(img.id + img.name)
        self._stopProgress(msg)
        return images

    def _get_ami_by_id(self,img):
        return "TODO"

    def _get_size(self,size):
        return "TODO"

    def _create_node(self,name,img,size):
        """
        Private method, creates instance from AMI.
        """
        driver = self._connect()
        node = driver.create_node(name='test', image=img, size=size)
        self.log.debug(node)

    @botcmd(split_args_with=' ')
    def aws_list_amis(self, msg, args):
        '''
        list all amis belonging to owner.
        '''
        self.log.debug("""
        from: {0}
        to: {1}
        is_direct: {2}
        is_group: {3}""".format(msg.frm,msg.to,msg.is_direct,msg.is_group))

        retVal = 'Images in region {0}: \n'.format(self.config['region'])
        imgs = self._list_amis(msg)
        for img in imgs:
            retVal += """id: `{0}`, name: `{1}`\n""".format(img.id,img.name)

        self.send(msg.frm,retVal)
