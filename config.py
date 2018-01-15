import os,logging,tempfile
# Slack Integration
BACKEND = 'Slack'

# OS Specific bot directories. Relative to current dir.
BOT_DATA_DIR = os.path.join(os.path.dirname(__file__),'data')
BOT_EXTRA_PLUGIN_DIR = os.path.join(os.path.dirname(__file__),'plugins')

# Logs are dumped to temp.
BOT_LOG_FILE = os.path.join(tempfile.gettempdir(), "errbot",'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@vish', )  # Specifies who is allowed to administrate the plugin.

BOT_IDENTITY = {
    'token': os.environ['ERRBOT_SLACK_TOKEN']
}

BOT_ALT_PREFIXES = ('@ramukaka',)

CHATROOM_PRESENCE = ()
