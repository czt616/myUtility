"""
Query class
"""

import os
import json
import sys
import re
import argparse
import codecs
from model import Model
from text import Text
from abc import ABCMeta,abstractmethod

class Query(object):
    """Base query class
    """
    def __init__(self,qid,query_text):
        self._qid = qid
        self._text_struct = Text(query_text)

    @property
    def original_model(self):
        return self._text_struct.raw_model()

    @property
    def text(self):
        return "%s" %self._text_struct
    



class ExpandedQuery(Query):
    """Queries with expansion
    """

    __metaclass__ = ABCMeta
    def __init__(self,qid,query_text,method,para_lambda):
        self._method,self._para_lambda = method, para_lambda
        super(ExpandedQuery,self),__init__(qid,query_text)
        self._expanding_model = None

    @abstractmethod
    def expand(self):
        pass

    @property
    def expanding_model(self):
        if not self._expanding_model:
            raise RuntimeError("Not expanded yet!")
        return self._expanding_model.raw_model()

    @property
    def method(self):
        return self._method

    @property
    def para_lambda(self):
        return self._para_lambda
    
    

    
    
    



# def main():
#     parser = argparse.ArgumentParser(description=__doc__)
#     parser.add_argument("")
#     args=parser.parse_args()

# if __name__=="__main__":
#     main()
