
try:
    from pkg_resources import resource_filename
except ImportError:
    def resource_filename(package_or_requirement, resource_name):
        return os.path.join(os.path.dirname(__file__), resource_name)
from myStemmer import pstem as stem
import re
import json


DATA_DIR = resource_filename('myUtility.misc','data')

def do_stem(matchobj):
    return stem(matchobj.group(0))


def get_stopwords(name=None):
    if not name:
        name = os.path.join(DATA_DIR,'stopwords.json')
    stopwords = json.load(open(name))
    return stopwords

