import logging


# logging config
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = '.'

class TestBotCommands:

    def _setup(self, testbot, config):
        testbot.push_message('!plugin config aws ' + str(config))
        msg = testbot.pop_message()
        assert 'plugin configuration done' in msg.lower()

    def test_aws_list_amis(self, testbot, config, constants):
        self._setup(testbot, config)
        testbot.push_message('!aws list amis')
        msg = testbot.pop_message()
        logger.info(msg)
        assert constants['TEST_AMI_ID'] in msg

    def test_aws_list_instances(self, testbot, config, constants):
        self._setup(testbot, config)
        testbot.push_message('!aws list instances')
        msg = testbot.pop_message()
        logger.info(msg)
        assert (
            constants['TEST_NODE_NAME'] in msg or
            "no nodes found" in msg
        )
    def test_aws_create_instance(self, testbot, config, constants):
        self._setup(testbot, config)
        testbot.push_message('!aws create instance')
        msg = testbot.pop_message()
        logger.info(msg)

