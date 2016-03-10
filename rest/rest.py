"""
base Rest API class
"""
from ..misc import crawl_url
from restexceptions import *
import json






class Rest(object):
    """
    Rest API base class
    """

    def __init__(self):
        self._END_POINT = ""

    def call_api(self,params):
        url, content = crawl_url(self._END_POINT, params)
        if url is None:
            return content
        else:
            raise ApiCallException(url)