"""
base wiki class
"""
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
        if url is not None:
            return content
        else:
            raise ApiCallException


