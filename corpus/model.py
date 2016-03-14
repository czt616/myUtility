"""
model related code
"""

import re
from myStemmer import pstem as stem 
from ..misc import do_stem

def update_model(model, text_string=None, text_list=None, text_dict=None):
    if text_string:
        for w in re.findall("\w+",text_string.lower()):
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


def update_stemmed_model(model, text_string=None, text_list=None, text_dict=None):
    if text_string:
        for w in re.findall("\w+",text_string.lower()) :
            w = stem(w)
            if w not in model:
                model[w] = 0
            model[w] += 1

    if text_list:
        for w in text_list:
            w = stem(w)
            if w not in model:
                model[w] = 0
            model[w] += 1


    if text_dict:
        for w in text_dict:
            w = stem(w)
            if w not in model:
                model[w] = 0
            model[w] += text_dict[w] 

