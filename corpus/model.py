"""
model related code
"""

import re
from myStemmer import pstem as stem 
from ..misc import do_stem
from corpusexceptions import *
import math

class Model(object):


    def __init__(self,no_stopwords,text_string=None, text_list=None, text_dict=None,
        need_stem = False, input_stemmed = False):
        self._need_stem = need_stem
        self._no_stopwords = no_stopwords
        self._model = {}
        self._normalized = False
        if text_string or text_list or text_dict:
            self.update(text_string=text_string, text_list=text_list, text_dict=text_dict,input_stemmed=input_stemmed)



    def __add__(self, other):
        if not isinstance(other, Model):
            raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" %type(self),type(other))

        elif self._need_stem != other._need_stem:
            raise ValueError(" Two model does not agree with stemming")
        elif self._no_stopwords != other._no_stopwords:
            raise ValueError(" Two model does not agree with stopword removal")
        else:
            if self._need_stem:
                new_obj = Model(self._no_stopwords,text_dict=self.model,need_stem=self._need_stem,input_stemmed=True)
                new_obj.update(text_dict = other.model, input_stemmed=True)
            else:
                new_obj = Model(self._no_stopwords,text_dict=self.model,need_stem=self._need_stem)
                new_obj.update(text_dict = other.model)
        return new_obj


    def __mul__(self,other):
        if not isinstance(other, (int,float)  ):
            raise TypeError("type %s not supported" %type(other))
        else:
            if self._need_stem:
                new_obj = Model(self._no_stopwords,text_dict=self.model,need_stem=self._need_stem,input_stemmed=True)
            else:
                new_obj = Model(self._no_stopwords,text_dict=self.model,need_stem=self._need_stem)
            for w in new_obj._model:
                new_obj._model[w] *= other
        return new_obj


    def __rmul__(self,other):
        return self*other

    def __div__(self,other):
        return self*(1.0/other)

    @property
    def model(self):
        return self._model
    
    
    

    def __update_model(self, text_string=None, text_list=None, text_dict=None):
        if not self.validate_input(text_string,text_list,text_dict):
            raise  TooManyInput

        if text_string:
            for w in re.findall("\w+",text_string.lower()):
                if w not in self._model:
                   self._model[w] = 0
                self._model[w] += 1

        if text_list:
            for w in text_list:
                if w not in self._model:
                    self._model[w] = 0
                self._model[w] += 1


        if text_dict:
            for w in text_dict:
                if w not in self._model:
                    self._model[w] = 0
                self._model[w] += text_dict[w]

        self._normalized = False


    def __update_stemmed_model(self, text_string=None, text_list=None, text_dict=None,input_stemmed=False):
        if not self.validate_input(text_string,text_list,text_dict):
            raise  TooManyInput

        if text_string:
            for w in re.findall("\w+",text_string.lower()) :
                if not input_stemmed:
                    w = stem(w)
                if w not in self._model:
                    self._model[w] = 0
                self._model[w] += 1

        if text_list:
            for w in text_list:
                if not input_stemmed:
                    w = stem(w)
                if w not in self._model:
                    self._model[w] = 0
                self._model[w] += 1


        if text_dict:
            for w in text_dict:
                if not input_stemmed:
                    w = stem(w)
                if w not in self._model:
                    self._model[w] = 0
                self._model[w] += text_dict[w] 



    def update(self,text_string=None, text_list=None, text_dict=None,input_stemmed=False):
        if not self.validate_input(text_string,text_list,text_dict):
            raise  TooManyInput


        if self._need_stem:
            self.__update_stemmed_model(text_string=text_string
                , text_list=text_list, text_dict=text_dict,input_stemmed=input_stemmed)

        elif input_stemmed:
            raise ValueError("cannot use stemmed input when the model is not stemmed model!\n")

        else:
            self.__update_model(text_string=text_string, text_list=text_list, text_dict=text_dict)


    def cosine_sim(self,other):
        if not isinstance(other, Model):
            raise TypeError("unsupported operand type(s) for cosine similarity: '%s' and '%s'" %type(self),type(other))
        elif self._need_stem != other._need_stem:
            raise ValueError(" Two model does not agree with stemming")
        elif self._no_stopwords != other._no_stopwords:
            raise ValueError(" Two model does not agree with stopword removal")
        else:
            self.normalize()
            other.normalize()
            dis = 0
            for w in self._model:
                if w in other.model:
                    dis += self._model[w] * other.model[w]
        return dis


    @staticmethod
    def validate_input(text_string,text_list,text_dict):

        if (text_string is not None and text_list is None and text_dict is None) or \
            (text_list is not None and text_string is None and text_dict is None) or \
            (text_dict is not None and text_list is None and text_string is None):
            return True

        else:
            return False




    def normalize(self): 
        if not self._normalized:  
            values = self._model.values()
            total = 0.0
            for v in values:
                total += v*v

            total = math.sqrt(total)

            for w in self._model:
                self._model[w] /= 1.0*total
            self._normalized = True