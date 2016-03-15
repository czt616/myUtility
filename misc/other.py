
try:
    from pkg_resources import resource_filename
except ImportError:
    def resource_filename(package_or_requirement, resource_name):
        return os.path.join(os.path.dirname(__file__), resource_name)
from myStemmer import pstem as stem
import re
import json


DATA_DIR = resource_filename('myUtility.misc','data')


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
    def get_stopwords(self,name=None):
        if not name:
            self.name = os.path.join(DATA_DIR,'stopwords.json')
        self.stopwords = json.load(open(self.name))
        
    def remove_stopwords_from_string(self,text_string):
        for w in self.stopwords:
            text_string = re.sub("(^|[^\w])"+w+"([^\w]|$)",rm_stopword,text_string,flags=re.I)
            

        return text_string


    def remove_stopwords_from_list(self,text_list):
        for w in self.stopwords:
            while w in text_list:
                text_list.remove(w)
        return text_list

    def remove_stopwords_from_dict(self,text_dict):
        for w in text_dict.keys():
            if w in stopwords:
                text_dict.pop(w,None)
        return text_dict