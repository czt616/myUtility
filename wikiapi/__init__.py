from ..misc import crawl_url
from wikipedia import Wikipedia
from wikidata import Wikidata


def get_default_configuration():
    _PARA = {
        'format':'json'
    }
    return _PARA


__all__ = ['Wikipedia', 'Wikidata']