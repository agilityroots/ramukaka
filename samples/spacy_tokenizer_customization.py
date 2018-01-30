"""

References:
1. https://spacy.io/api/tokenizer
1. https://github.com/explosion/spaCy/issues/396
"""
import spacy
nlp = spacy.load('en_core_web_lg')
from spacy.attrs import ORTH, LEMMA
from spacy.tokenizer import Tokenizer
exceptions = [
    {"us":[
            {
                ORTH: "us"
            },
            {
                ORTH: "-east", LEMMA: "east"
            }
        ]
    }
]
tokenizer = Tokenizer(nlp.vocab)
tokenizer.add_special_case("""us-east-1""", exceptions)