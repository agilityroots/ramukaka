import random
from errbot import botcmd, BotPlugin, botmatch
class TimePass(BotPlugin):

    # example flow copied from
    # https://github.com/errbotio/err-guess-a-number
    @botcmd
    def tryme(self, msg, _):
        """Start to guess a number !"""
        msg.ctx['tries'] = 10
        msg.ctx['to_guess'] = random.randint(0,99)
        return 'Guess a number between 0 and 99 !'

    @botmatch(r'^\d{1,2}$', flow_only=True)
    def guessing(self, msg, match):
        guess = int(match.string)
        to_guess = msg.ctx['to_guess']
        if guess == to_guess:
            msg.ctx['tries'] = 0
            return 'You won !'

        msg.ctx['tries'] -= 1
        if msg.ctx['tries'] == 0:
            return 'No more tries, you lost!'

        if guess < to_guess:
            return 'More ! %d tries left' % msg.ctx['tries']

        return 'Less! %d tries left' % msg.ctx['tries']

    # trying to replicate same flow with NLP

    @botcmd
    def timepass(self,msg,_):
        """Starts the Timepass Flow."""
        self.log.debug(str(msg))
        msg.ctx['should_end'] = False
        return """Tell Me What To Do :+1:"""

    @botmatch(r'^.*coffee.*$', flow_only=True)
    def timepassing_coffee(self,msg,match):
        msg.ctx['should_end'] = False
        msg.ctx['orig_msg'] = str(msg)
        return """Here is some :coffee: <br> your input: {0} match: {1}""".format(msg,match.string)

    @botmatch(r'^.*tea.*$', flow_only=True)
    def timepassing_tea(self,msg,match):
        msg.ctx['should_end'] = False
        msg.ctx['orig_msg'] = str(msg)
        return """Here is some :tea: <br> your input: {0} match: {1}""".format(msg,match.string)
