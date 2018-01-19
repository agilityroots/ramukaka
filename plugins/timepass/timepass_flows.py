from errbot import botflow, FlowRoot, BotFlow, FLOW_END
class TimepassFlows(BotFlow):
    """ Conversation flows related to polls"""

    # replicating this flow
    @botflow
    def timepass(self, flow: FlowRoot):
        """This flow understands user's timepass needs and routes his requests."""
        tp_parser = flow.connect('parse_input',auto_trigger=True)
        tp_command = tp_parser.connect('err_bail',predicate=lambda ctx: 'intent' in ctx and ctx['intent'] == '')
        tp_command = tp_parser.connect('do_timepass',predicate=lambda ctx: 'intent' in ctx and ctx['intent'] != '')
