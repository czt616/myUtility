"""
Text class
"""


import re
import warnings
from model import Model

class Text(object):
    def __init__(self,text):
        self._text = text

    @property
    def text(self):
        return self._text
    
    @property
    def stemmed_text(self):
        if not self._stemmed_text:
            self._stemmed_text = re.sub("\w+",do_stem, self._text.lower())
        return self._stemmed_text

    # @stemmed_text.setter
    # def stemmed_text(self,text):
    #     self._stemmed_text = text

    @property
    def raw_model(self):
        if not self._raw_model:
            self._raw_model = Model(text_string=self.text,need_stem = False)
        return self._raw_model

    # @model.setter
    # def model(self, text_list=None, text_dict=None):
    #     if not self._model:
    #         self._model = {}
    #         update_model(self._model,text_list=text_list, text_dict = text_dict)
    #     return self._model


    @property
    def stemmed_model(self):
        if not self._stemmed_model:
            self._stemmed_model = Model(text_string=self._stemmed_text,need_stem = True, input_stemmed=True)
        return self._stemmed_model
    

