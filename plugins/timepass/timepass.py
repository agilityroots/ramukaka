import random,spacy
from errbot import botcmd, BotPlugin, botmatch
class TimePass(BotPlugin):

    def get_intent(self,orig_msg):

        """
        Use NLP to convert message into an Intent.
        """
        model = 'sm'
        nlp = spacy.load('en_core_web_' + model)
        coffee = nlp('coffee')
        tea = nlp('tea')
        orig = nlp(orig_msg)
        cm = orig.similarity(coffee)
        ct = orig.similarity(tea)
        d = float(abs(cm-ct) / cm)
        self.log.debug("NLP MEASURE for {0}: coffee {1}, tea {2}, distance: {3}".format(orig_msg,cm,ct,d))

        # values too close together? warn user.
        if (cm > ct and d >= 0.1):
            return 'coffee'
        elif (ct > cm and d>=0.1):
            return 'tea'
        else:
            return ''

    @botmatch(r'^[a-zA-Z\s]+$',hidden=True)
    def parse_input(self,msg,_):
        if self._bot.mode == "slack":
            self._bot.add_reaction(msg, "hourglass")
        else:
            yield "In Progress..."
        msg.ctx['orig_msg'] = str(msg)
        msg.ctx['intent'] = self.get_intent(str(msg))
        if self._bot.mode == "slack":
            self._bot.remove_reaction(msg, "hourglass")
        else:
            yield "Done!"
        self.log.debug('parsed orig msg {0} got intent: {1} '.format(msg.ctx['orig_msg'],msg.ctx['intent']))

    @botcmd(flow_only=True)
    def do_timepass(self,msg,_):
        self.send(msg.frm,""":{0}:""".format(msg.ctx['intent']))


    @botcmd(flow_only=True)
    def err_bail(self,msg,_):
        self.send(msg.frm,
            """
:thinking_face:
I am not entirely sure what you asked for.
You entered: {0} But I only accept requests for 'coffee' or 'tea'
""".format(msg.ctx['orig_msg']))
