"""
Simple script for trying out spaCy NLP. (https://spacy.io/)

INPUTS

Try:

list my aws instances
I would like to get a list of instances in aws.
can you list running aws instances?
get me a list of ec2 instances in useast1 region.


### Spacy Model Links

* SpaCy's `en` model (small sized, 35 MB, but less accurate):
https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-2.0.0

A larger (800MB), more accurate model:
https://github.com/explosion/spacy-models/releases/tag/en_core_web_lg-2.0.0

"""

import sys
import spacy
from spacy.tokens import Token, Span
from spacy.symbols import nsubj, VERB
MODEL = 'lg'
NLP = spacy.load('en_core_web_' + MODEL)
ALLOWED_VERBS = ['list', 'create', 'delete','give', 'get']
ALLOWED_VERBS_DOCS = [NLP(i) for i in ALLOWED_VERBS]
ALLOWED_TOPICS = ['aws']
ALLOWED_TOPICS_DOCS = [NLP(i) for i in ALLOWED_TOPICS]

ALLOWED_CMDS = ['instance']
ALLOWED_CMDS_DOCS = [NLP(i) for i in ALLOWED_CMDS]

ALLOWED_ARGS = ['instance', 'region']
ALLOWED_ARGS_DOCS = [NLP(i) for i in ALLOWED_ARGS]
MIN_CONFIDENCE = 0.5
VERB_CODE = 99

def find_verbs(doc):
    """
    given a raw input string, find verbs.
    
    Reference:
    https://spacy.io/usage/spacy-101#annotations-pos-deps
    """
    print("TEXT | LEMMA | POS | TAG | DEP | SHAPE | IS_ALPHA | IS_STOP")
    print("---------------------------------------------")
    for token in doc:
        print("%s | %s | %s(%d) | %s(%d) | %s | %s | %s | %s " %
              (token.text, token.lemma_, token.pos_, token.pos, token.tag_, token.tag, token.dep_,
               token.shape_, token.is_alpha, token.is_stop))


    return [token for token in doc if token.pos == VERB_CODE]

def split(doc):
    """
    process the document 
    
    - split doc into a set of noun chunks.
    - in each noun chunk check if root text is a 'dobj' (direct object) is present.
    - a dobj represents the object on which an action has to be done , i.e. the COMMAND.
    - further check if the dobj has a verb as its root.head.text. This represents the action to be done 
    - on the root object.
    - every other noun chunk represents arguments for the command.

    """
    get_possible_args = lambda span: [span.root.text for arg in ALLOWED_ARGS_DOCS if span.root.similarity(arg) > MIN_CONFIDENCE] 
    get_arg_qualifier = lambda span: [s.text for s in span if s.dep_ == 'compound']
    is_argument = lambda span: span.root.dep_ == 'pobj'
    is_command = lambda span: span.root.dep_ == 'dobj' and span.root.head.text in ALLOWED_VERBS
    Span.set_extension('is_argument',getter=is_argument)
    Span.set_extension('is_command',getter=is_command)
    Span.set_extension('get_possible_args',getter=get_possible_args)
    Span.set_extension('get_arg_qualifier',getter=get_arg_qualifier)
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
          chunk.root.head.text)
        if chunk._.is_command:
            print ("command: {}".format(chunk.root.head.text))
            print ("object on which command has to be done: {}".format(chunk))
        if chunk._.is_argument:
            print("raw argument: {}".format(chunk))
            print("possible arguments: {}".format(chunk._.get_possible_args))
            print("argument qualifiers: {}".format(chunk._.get_arg_qualifier))

def get_command(doc):
    """
    Reference:
    https://spacy.io/api/token#set_extension
    """
    verb_tokens = find_verbs(doc)

    possible_commands = [{v : a}
                         for v in verb_tokens
                         for a in ALLOWED_VERBS_DOCS
                         if v.similarity(a) > MIN_CONFIDENCE]

    if not possible_commands or len(possible_commands) > 1:
        print("ambiguous statement: possible commands: {}".format(possible_commands))
    else:
        print(possible_commands)
print("type a single sentence:")
data = sys.stdin.readline()
nlp_doc = NLP(data)
get_command(nlp_doc)
split(nlp_doc)