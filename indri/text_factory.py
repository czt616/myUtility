"""
Factory for generating trec text from document
"""

import os
import json
import sys
import re
import argparse
import codecs

from templates import *
from ..misc import gene_single_indri_text


class TextFactory(object):
    """factory for generating trec text from  plane text

    """
    def __init__(self,dest_file_path):
        self._dest_file_path = dest_file_path
        self._documents = []

    def add_document(self,did,original_text,extra_fields=None,
        field_data=None):
        single_document_text = gene_single_indri_text(did,original_text,extra_fields,field_data)
        if single_document_text is not None:
            self._documents.append()

        

    def write(self):
        with codecs.open(self._dest_file_path, 'w','utf-8') as f:
            for document in self._documents:
                f.write(document+"\n")
        

# def main():
#     parser = argparse.ArgumentParser(description=__doc__)
#     parser.add_argument("")
#     args=parser.parse_args()




# if __name__=="__main__":
#     main()

