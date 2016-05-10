"""
get data from Wikidata api
"""

from wikibase import *
from wikipedia import Wikipedia
import time
from collections import Iterable


class Wikidata(Wikibase):
    """
    Wikidata class
    """

    def __init__(self):
        self._END_POINT="https://www.Wikidata.org/w/api.php?"

    

    def get_entity_info_by_name(self,name):
        entity = {}
        params = self.get_default_configuration()
        params['action'] = 'wbgetentities'
        params['sites'] = 'enwiki'
        params['titles'] = name
        params['normalize'] = 1

        content = self.call_api(params)
        try:
            result = json.loads(content)
        except ValueError:
            raise ResultErrorException(content,"mal-formatted")
        else:
            try:
                entities = result['entities']
            except KeyError:
                raise ResultErrorException(content,"unexpected result structure")
            else:
                if len(entities) != 1:
                    raise ResultErrorException(content,"More than one entities have the same name!")
                else:
                    eid = entities.keys()[0] #entity id
                    entity['eid'] = 'Q'+str(eid)
                    try:
                        entity['description'] = entities[eid]['descriptions']['en']['value']
                    except KeyError:
                        # if no description, put empty string in it
                        entity['description'] = ""
                    try:   
                        classes = entities[eid]['claims']['P31'] #class info
                    except KeyError:
                        raise NoClassException(content,name)
                    else:
                        cids = []
                        for c in classes:
                            cid = 'Q'+str(c['mainsnak']['datavalue']['value']['numeric-id'])
                            cids.append(cid)
                        entity["class_info"] = self.get_class_info(cids)
                        return entity


    def get_class_info(self,cids):
        class_info = {}
        params = self.get_default_configuration()
        params['action'] = 'wbgetentities'
        params['ids'] = "|".join(cids)
        params['props'] = 'labels'
        content = self.call_api(params)
        try:
            result = json.loads(content)
        except ValueError:
            raise ResultErrorException(content,"mal-formatted")
        else:
            for cid in cids:
                try:
                    class_info[cid] = result['entities'][cid]['labels']['en']['value']

                except KeyError:
                    continue
            else:
                if len(class_info) ==0:
                    class_info = None
                return class_info



