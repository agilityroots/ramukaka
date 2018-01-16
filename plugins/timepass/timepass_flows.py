from errbot import botflow, FlowRoot, BotFlow, FLOW_END
import spacy
class TimepassFlows(BotFlow):
    """ Conversation flows related to polls"""

    def is_coffee(orig_msg):
        model = 'sm'
        nlp = spacy.load('en_core_web_' + model)
        coffee = nlp('i want coffee')
        orig = nlp(orig_msg)
        similarity = orig.similarity(coffee)
        if (orig > 0.5):
            return True
        else:
            return False

    # example flow copied from
    # https://github.com/errbotio/err-guess-a-number

    @botflow
    def guess(self, flow: FlowRoot):
        """ This is a flow that can set a guessing game."""
        # setup Flow
        game_created = flow.connect('tryme', auto_trigger=True)
        one_guess = game_created.connect('guessing')
        one_guess.connect(one_guess)  # loop on itself
        one_guess.connect(FLOW_END, predicate=lambda ctx: ctx['tries'] == 0)

    # replicating this flow
    @botflow
    def timepass(self, flow: FlowRoot):
        """This flow understands user's timepass needs and routes his requests."""
        tp_created = flow.connect('timepass',auto_trigger=True)
        tp_command = tp_created.connect('timepassing_coffee',predicate=lambda ctx: self.is_coffee(ctx['orig_msg']))
        tp_command = tp_created.connect('timepassing_tea',predicate=lambda ctx: self.is_coffee(ctx['orig_msg']) == False)
        tp_command.connect(FLOW_END,predicate=lambda ctx: ctx['should_end'] == True)
