
try:
    from pkg_resources import resource_filename
except ImportError:
    def resource_filename(package_or_requirement, resource_name):
        return os.path.join(os.path.dirname(__file__), resource_name)

import re
import json
import os
import copy
import warnings
try:
    from myStemmer import pstem as stem
except ImportError:
    def stem(input):
        return input
    warnings.warn("No module myStemmer in this machine!")

DATA_DIR = resource_filename('myUtility.misc','data')

def get_stopwords():
    return json.load(open(os.path.join(DATA_DIR,'stopwords.json'))).keys()


def rm_stopword(m):
    r = ""
    if m.group(1) is not None:
      r = m.group(1)
    if m.group(2) is not None:
      r += m.group(2)
    return r



def do_stem(matchobj):
    return stem(matchobj.group(0))


class Stopword_Handler(object):
    def __init__(self,name=None):
        if not name:
            self.name = os.path.join(DATA_DIR,'stopwords.json')
        self.stopwords = json.load(open(self.name))
    
    def remove_stopwords(self,input_data):
        if isinstance(input_data,str):
            return self._remove_stopwords_from_string(input_data)
        elif isinstance(input_data,list):
            return self._remove_stopwords_from_list(input_data)
        elif isinstance(input_data,dict):
            return  self._remove_stopwords_from_dict(input_data)
        else:
            raise TypeError("Does not support type %s" %(type(input_data)))

    def _remove_stopwords_from_string(self,text_string):
        temp_data = text_string
        for w in self.stopwords:
            temp_data = re.sub("(^|[^\w])"+w+"([^\w]|$)",rm_stopword,temp_data,flags=re.I)
            

        return temp_data


    def _remove_stopwords_from_list(self,text_list):
        temp_data = text_list[:]

        for w in self.stopwords:
            while w in temp_data:
                temp_data.remove(w)
        return temp_data

    def _remove_stopwords_from_dict(self,text_dict):
        temp_data = copy.deepcopy(text_dict)
        for w in temp_data.keys():
            if w in stopwords:
                temp_data.pop(w,None)
        return temp_data
