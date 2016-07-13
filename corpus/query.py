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
        self._text = query_text
        self._text_struct = Text(query_text)

    @property
    def original_model(self):
        return self._text_struct.raw_model()

    @property
    def text(self):
        return "%s" %self._text
    



class ExpandedQuery(Query):
    """Queries with expansion
    """

    def __init__(self,qid,query_text,para_lambda):
        self._para_lambda =  para_lambda
        super(ExpandedQuery,self),__init__(qid,query_text)
        self._expanding_model = None

    
    def expand(self,expanding_term_weights):
        self._expanding_model = Model(False,text_dict=expanding_term_weights)

    @property
    def expanding_model(self):
        if not self._expanding_model:
            raise RuntimeError("Not expanded yet!")
        return self._expanding_model.raw_model()


    @property
    def para_lambda(self):
        return self._para_lambda
    
    

    
    
    



# def main():
#     parser = argparse.ArgumentParser(description=__doc__)
#     parser.add_argument("")
#     args=parser.parse_args()

# if __name__=="__main__":
#     main()

