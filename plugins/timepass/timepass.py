from errbot import BotPlugin, botcmd, cmdfilter
import spacy
class TimePass(BotPlugin):


    def is_similar(input):
        return True

    # http://errbot.io/en/latest/errbot.html#errbot.cmdfilter
    @cmdfilter
    def understand_cmd(self, msg, cmd, args, dry_run):
        """
        :param msg: The original chat message.
        :param cmd: The command name itself.
        :param args: Arguments passed to the command.
        :param dry_run: True when this is a dry-run.
           Dry-runs are performed by certain commands (such as !help)
           to check whether a user is allowed to perform that command
           if they were to issue it. If dry_run is True then the plugin
           shouldn't actually do anything beyond returning whether the
           command is authorized or not.
           """
        # Otherwise pass data through to the (potential) next filter:
        self.log.debug("************* Message: " + str(msg) + ", command: " + str(cmd))
        return msg, cmd, args

    @botcmd
    def get_me_some_tea(self, msg, args):

        """
        gives you tea
        """
        return """
        :tea:
        """
    @botcmd
    def get_me_some_coffee(self, msg, args):
        """
        gives you coffee
        """

        return """
        :coffee:
        """
