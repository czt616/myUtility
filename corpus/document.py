"""
document class
"""

import codecs
from sentence import Sentence
from text import Text
from corpusexceptions import *
from nltk.tokenize import sent_tokenize
import re
from myUtility.misc import Stopword_Handler



class Document(Text):
    def __init__(self,did,file_path=None,text=None,sentences=None,remove_stopwords=False):
        if self.validate_input(file_path=file_path,text=text,sentences=sentences):
            self._text = ""
            self._remove_stopwords = remove_stopwords
            if file_path:
                with codecs.open(file_path,'r','utf-8') as f:
                    self._text = f.read()
            elif text:
                self._text = text
                if remove_stopwords:
                    stopword_handler = Stopword_Handler()
                    self._text = stopword_handler.remove_stopwords_from_string(self._text)
                
            self._did = did
            if sentences:
                self._sentences = []
                if remove_stopwords:
                    stopword_handler = Stopword_Handler()
                    sentences = map(stopword_handler.remove_stopwords_from_string,sentences)
                for sentence in sentences:    
                    self.add_sentence(sentence)

        else:
            raise  TooManyInput

    def split_sentences(self):
        for sentence in sent_tokenize(self.text):
            self.add_sentence(sentence)



    def add_sentence(self,text):
        self._sentences.append(Sentence(text))
        self._text += "\n%s" %text
    

    @property
    def sentences(self ):
        try:
            return self._sentences
        except AttributeError:
            self._sentences = []
            self.split_sentences()
            return self._sentences
    
    @staticmethod
    def validate_input(file_path,text,sentences):

        if (file_path is not None and text is None and sentences is None) or \
            (text is not None and file_path is None and sentences is None) or \
            (sentences is not None and text is None and file_path is None):
            return True

        else:
            return False