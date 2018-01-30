import random
import spacy
from spacy.tokens import Token, Span
from spacy.symbols import nsubj, VERB
from errbot import botcmd, BotPlugin, botmatch

LANG_MODEL = 'lg'
NLP = spacy.load('en_core_web_' + LANG_MODEL)
MIN_CONFIDENCE = 0.5
MODEL = {
    "verbs": ['list', 'create', 'delete', 'give', 'get'],
    "keywords": ['aws'],
    "cmd_qualifiers": ['instances'],
    "args": ['instance', 'region']
}
ALLOWED_VERBS_DOCS = [NLP(i) for i in MODEL['verbs']]
ALLOWED_TOPICS_DOCS = [NLP(i) for i in MODEL['keywords']]
ALLOWED_ARGS_DOCS = [NLP(i) for i in MODEL['args']]
ALLOWED_CMDQUAL_DOCS = [NLP(i) for i in MODEL['cmd_qualifiers']]

class Router(BotPlugin):

    def get_intent(self,orig_msg):

        """
        Use NLP to convert message into
        - command
        - keyword
        - arguments.

        Process
        - split doc into a set of noun chunks.
        - in each noun chunk check if root text is a 'dobj' (direct object).
        - a dobj represents the object on which an action has to be done , i.e. the COMMAND.
        - further check if the dobj has a verb as its root.head.text. This represents the action to be done 
        - on the root object.
        - every other noun chunk represents arguments for the command.

        """
        is_command = lambda span: span.root.dep_ == 'dobj' and span.root.head.text in MODEL['verbs']
        get_cmd_qualifier = lambda span: [span.root.text for arg in ALLOWED_CMDQUAL_DOCS 
                                          if span.root.similarity(arg) > MIN_CONFIDENCE][0]

        is_argument = lambda span: span.root.dep_ == 'pobj'
        get_arg = lambda span: [span.root.text for arg in ALLOWED_ARGS_DOCS 
                                if span.root.similarity(arg) > MIN_CONFIDENCE][0]
        get_arg_qualifier = lambda span: [s.text for s in span if s.dep_ == 'compound'][0]

        Span.set_extension('is_argument', getter=is_argument)
        Span.set_extension('is_command', getter=is_command)
        Span.set_extension('get_arg', getter=get_arg)
        Span.set_extension('get_arg_qualifier', getter=get_arg_qualifier)
        Span.set_extension('get_cmd_qualifier', getter=get_cmd_qualifier)
        doc = NLP(orig_msg)
        return_value = {
            'cmd': [],
            'cmd_qualifiers': [],
            'keywords': [],
            'args': [],
            'arg_qualifiers': []
            }


        # get keyword from entire doc.
        return_value['keywords'].append([s.text for s in doc if s.text in MODEL['keywords']])

        # process noun chunks and retrieve all commands, args.
        for chunk in doc.noun_chunks:
            self.log.debug("chunk: {0}, root.text: {1}, root.dep: {2}, root.head.text: {3}"
                           .format(chunk.text, chunk.root.text,
                                   chunk.root.dep_, chunk.root.head.text))


            if chunk._.is_command:
                return_value['cmd'].append(chunk.root.head.text)
                return_value['cmd_qualifiers'].append(chunk._.get_cmd_qualifier)
                self.log.debug ("found command: {}".format(chunk.root.head.text))
            if chunk._.is_argument:
                self.log.debug("{0}, {1}".format(
                        chunk._.get_arg,
                        [chunk.root.similarity(i) for i in ALLOWED_ARGS_DOCS]
                    )
                    )
                return_value['args'].append(chunk._.get_arg)
                return_value['arg_qualifiers'].append(chunk._.get_arg_qualifier)

        return return_value

    @botmatch(r'^[a-zA-Z0-9-\s]+$',hidden=True)
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
        self.send(msg.frm, str(msg.ctx['intent']))

    @botcmd(flow_only=True)
    def aws_route(self, msg, args):
        list_instances = self.get_plugin('aws').aws_list_instances

        func_mapper = {
            'list': {
                'instances': self.get_plugin('aws').aws_list_instances
            }
        }

        parsed = msg.ctx['intent']
        func_mapper[parsed['cmd'][0]][parsed['cmd_qualifiers'][0]](msg, args)

        # if 'list' in parsed['cmd']:
        #     if 'instances' in parsed['cmd_qualifiers']:
        #         list_instances(msg, args)


    @botcmd(flow_only=True)
    def err_bail(self,msg,_):
        self.send(msg.frm,
            """
:thinking_face:
I am not entirely sure what you asked for.
You entered: {0} But I only accept requests for 'coffee' or 'tea'
""".format(msg.ctx['orig_msg']))
