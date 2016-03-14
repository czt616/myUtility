"""
Text class
"""


import re
from ..misc import do_stem


def update_model(model, text_string=None, text_list=None, text_dict=None):
    if text_string:
        for w in re.findall("\w+",text_string):
            if w not in model:
                model[w] = 0
            model[w] += 1

    if text_list:
        for w in text_list:
            if w not in model:
                model[w] = 0
            model[w] += 1


    if text_dict:
        for w in text_dict:
            if w not in model:
                model[w] = 0
            model[w] += text_dict[w] 




class Text(object):
    def __init__(self,text):
        self._text = text

    @property
    def text(self):
        return self._text
    
    @property
    def stemmed_text(self):
        self._stemmed_text = re.sub("\w+",do_stem, self._text.lower())
        return self._stemmed_text

    @property
    def model(self):
        self._model = {}
        update_model(self._model,text_string=self.text)
        return self._model

    @property
    def stemmed_model(self):
        self._stemmed_model = {}
        update_model(self._stemmed_model,text_string=self.stemmed_text)
        return self._stemmed_model
    

