"""
base wiki class
"""
from ..misc import crawl_url
from wikiexceptions import *
import json






class Wikibase(object):
    """
    Wikidata class
    """

    def __init__(self):
        self._END_POINT = ""

    def call_api(self,params):
        url, content = crawl_url(self._END_POINT, params)
        if url is None:
            return content
        else:
            raise ApiCallException(url)

    @staticmethod
    def get_default_configuration():
        _PARA = {
            'format':'json'
        }
        return _PARA


