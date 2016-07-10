"""
Text class
"""


import re
import warnings
from model import Model
from ..misc import do_stem,Stopword_Handler

class Text(object):
    def __init__(self,text,remove_stopwords=False):
        self._text = text
        self._no_stopwords = remove_stopwords
        if remove_stopwords:
                stopword_handler = Stopword_Handler()
                self._text = stopword_handler.remove_stopwords_from_string(self._text)

    @property
    def text(self):
        return self._text
    
    @property
    def stemmed_text(self):
        try:
            return self._stemmed_text
        except AttributeError:
            self._stemmed_text = re.sub("\w+",do_stem, self._text.lower())
            return self._stemmed_text

    # @stemmed_text.setter
    # def stemmed_text(self,text):
    #     self._stemmed_text = text

    @property
    def raw_model(self):
        try :
            return self._raw_model
        except AttributeError:
            self._raw_model = Model(self._no_stopwords,text_string=self.text,need_stem = False)
            return self._raw_model

    # @model.setter
    # def model(self, text_list=None, text_dict=None):
    #     if not self._model:
    #         self._model = {}
    #         update_model(self._model,text_list=text_list, text_dict = text_dict)
    #     return self._model


    @property
    def stemmed_model(self):
        try:
            return self._stemmed_model
        except AttributeError:
            self._stemmed_model = Model(self._no_stopwords,text_string=self.stemmed_text,need_stem = True, input_stemmed=True)
            return self._stemmed_model
    
    @property
    def length(self):
        try:
            return self._length
        except AttributeError:
            self._length = len(re.findall("\w+",self._text))
            return self._length
    
