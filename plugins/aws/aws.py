from errbot import BotPlugin, botcmd
from optparse import OptionParser
import os
import time
import logging
from awsadapter import AwsAdapter
logging.basicConfig(level=logging.DEBUG)

class Aws(BotPlugin):

    def _startProgress(self, msg):
        '''
        backend-specific indicator of progress
        '''
        if self._bot.mode == "slack":
            self._bot.add_reaction(msg, "hourglass")
        else:
            yield "..."

    def _stopProgress(self, msg):
        '''
        backend-specific indicator of progress
        '''

        if self._bot.mode == "slack":
            self._bot.remove_reaction(msg, "hourglass")
        else:
            yield "..."

    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'access_id': os.environ['ERRBOT_AWS_ACCESS_KEY'],
            'secret_key': os.environ['ERRBOT_AWS_SECRET_KEY'],
            'account_id': os.environ['ERRBOT_AWS_ACCOUNT_ID'],
            'region': os.environ['ERRBOT_AWS_DEFAULT_REGION'],
            'keypair': os.environ['ERRBOT_AWS_KEYPAIR_NAME'],
        }
        return config

    @botcmd(split_args_with=' ')
    def aws_create_instance(self, msg, args):
        '''
        create instance
        '''
        node = AwsAdapter(self.config).create_node(
            name="test_node",
            img="ami-c24ef5bb",
            size="t2.micro")
        self.send(msg.frm, "{0} node".format(str(node)))

    @botcmd(split_args_with=' ')
    def aws_list_instances(self, msg, args):
        '''
        list instances
        '''
        nodes = AwsAdapter(self.config).list_instances()
        self.send(msg.frm, len(nodes) > 0 and str(nodes) or "no nodes found")

    @botcmd(split_args_with=' ')
    def aws_list_amis(self, msg, args):
        '''
        list all amis belonging to owner.
        '''
        retVal = 'Images:\n'
        imgs = AwsAdapter(self.config).list_amis()
        for img in imgs:
            retVal += """id: `{0}`, name: `{1}`\n""".format(img.id,img.name)

        self.send(msg.frm,retVal)
