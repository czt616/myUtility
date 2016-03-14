"""
document class
"""

import os
import json
import sys
import re
from ..misc import do_stem
from corpus import Sentence,Text


class Document(Text):
    def __init__(self,did,text):
        self._text = text
        self._did = did
        self.sentences = []


    def add_sentence(self,text):
        self.sentences.append(Sentence(text))
    
