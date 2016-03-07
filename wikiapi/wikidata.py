"""
get data from Wikidata api
"""

from wikibase import *

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
            entities = result['entities']
            if len(entities) != 1:
                print "More than one entities have the same name!"
                raise ResultErrorException(content)
            else:
                eid = entities.keys()[0] #entity id
                entity['eid'] = 'Q'+str(eid)
                entity['description'] = entities[eid]['descriptions']['en']['value']
                entity['class_id'] = {}
                classes = entities[eid]['claims']['P31'] #class info
                cids = []
                for c in classes:
                    cid = 'Q'+str(c['mainsnak']['datavalue']['value']['numeric-id'])
                    cids.append(cid)
                entity["class_info"] = self.get_class_info(cids)

        except Exception as e:
            print e
            raise ResultErrorException(content)

        else:
            return entity


    def get_class_info(self,cids):
        class_info = {}
        params = self.get_default_configuration()
        params['action'] = 'wbgetentities'
        params['ids'] = "|".join(cids)
        params['prors'] = 'labels'
        content = self.call_api(params)
        try:
            result = json.loads(content)
            for cid in cids:
                class_info[cid] = result['entities'][cid]['labels']['en']['value']

        except Exception as e:
            print e
            raise ResultErrorException(content)
        else:
            return class_info





def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("")
    args=parser.parse_args()

if __name__=="__main__":
    main()

