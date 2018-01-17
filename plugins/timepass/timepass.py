import random,spacy
from errbot import botcmd, BotPlugin, botmatch
class TimePass(BotPlugin):

    def get_intent(self,orig_msg):
        model = 'sm'
        nlp = spacy.load('en_core_web_' + model)
        coffee = nlp('coffee')
        tea = nlp('tea')
        orig = nlp(orig_msg)
        cm = orig.similarity(coffee)
        ct = orig.similarity(tea)
        self.log.debug("NLP MEASURE for {0}: coffee {1}, tea {2}".format(orig_msg,cm,ct))
        if (cm > ct):
            return 'coffee'
        else:
            return 'tea'

    @botmatch(r'^[a-zA-Z\s]+$',hidden=True)
    def parse_input(self,msg,_):
        msg.ctx['orig_msg'] = str(msg)
        msg.ctx['intent'] = self.get_intent(str(msg))
        self.log.debug('>>>>>>>>>>>>>>>> parsed orig msg {0} for an intent: {1} '.format(msg.ctx['orig_msg'],msg.ctx['intent']))

    @botcmd(flow_only=True)
    def timepassing_coffee(self,msg,_):
        return """You asked for {0}. Here is some :coffee: <br>""".format(msg.ctx['intent'])

    @botcmd(flow_only=True)
    def timepassing_tea(self,msg,_):
        return """You asked for {0}. Here is some :tea: <br>""".format(msg.ctx['intent'])
