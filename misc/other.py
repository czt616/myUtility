from myStemmer import pstem as stem
import re

def do_stem(matchobj):
    return stem(matchobj.group(0))