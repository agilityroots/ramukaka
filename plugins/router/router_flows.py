from errbot import botflow, FlowRoot, BotFlow, FLOW_END
class RouterFlows(BotFlow):
    """ Conversation flows related to polls"""

    @botflow
    def timepass(self, flow: FlowRoot):
        """This flow understands user's request and routes to appropriate plugin."""
        router = flow.connect('parse_input',auto_trigger=True)
        tp_command = router.connect('aws_route', predicate = lambda ctx: 'intent' in ctx)
        tp_command = tp_parser.connect('err_bail',predicate=lambda ctx: 'intent' in ctx and ctx['intent'] == '')
        # tp_command = tp_parser.connect('do_timepass',predicate=lambda ctx: 'intent' in ctx and ctx['intent'] != '')
