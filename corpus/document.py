"""
document class
"""

import os
import json
import sys
import re
from ..misc import do_stem
from corpus import Sentence,Text
from nltk.tokenize import sent_tokenize

class Document(Text):
    def __init__(self,did,text=None,sentences=None):
        self._text = ""
        if text:
            self._text = text
        self._did = did
        self._sentences = []
        if sentences:
            for sentence in sentences:
                self.add_sentence(sentence)


    def split_sentences(self):
        for sentence in sent_tokenize(self.text):
            self.add_sentence(sentence)



    def add_sentence(self,text):
        self._sentences.append(Sentence(text))
        self._text += "\n%s" %text
    

    @property
    def sentences(self ):
        if not self._sentences:
            self.split_sentences()
        return self._sentences
        