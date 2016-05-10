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




class WikiCategory(Object):
    def get_single_entity_cate(entity,wikipedia_caller,wikidata_caller):
        """
        find the category info for a single entity

        Returns:
        -----------------------------------------
        entitiy_class_list: a list of categories of the entity

        """


        try:
            entity_name = wikipedia_caller.get_entity_name(entity)
        except wikiexceptions.ResultErrorException:
            print "cannot find an entity for name %s" %entity
            return None
        try:
            entity_info = wikidata_caller.get_entity_info_by_name(entity_name)
        except wikiexceptions.NoClassException:
            print "entity %s has no class info" %entity_name
            return None

        else:
            return entity_info['class_info']


    def get_cate_for_entity_iterable(entity_iterable,wikipedia_caller,wikidata_caller):
        """
        find the categories info for an Iterable of entities

        Returns:
        -----------------------------------------
        cate_info: a dict categories of the entities

                    key: entity name
                    value: a list of categories of the key

        """
        wikipedia_caller = Wikipedia()
        wikidata_caller = Wikidata()
        cate_info = {}
        for entity in entity_iterable:
            result =  get_single_entity_cate(entity,wikipedia_caller,wikidata_caller)
            time.sleep(5)
            if not result:
                cate_info[entity] = None
            else:
                cate_info[entity] = []
                for cid in result:
                    cate_info[entity].append(result[cid])
        return cate_info



    def get_cates(entitiy_input):
        """
        Find the categories info for entities. Do type check
        first and support both string and Iterable(except dict)
        input 

        Returns:
        -----------------------------------------
        cate_info: a dict categories of the entities

                    key: entity name
                    value: a list of categories of the key

        """
        wikipedia_caller = Wikipedia()
        wikidata_caller = Wikidata()
        input_type = type(entitiy_input)
        if isinstance(entitiy_input,Iterable):
            if type(entitiy_input) == str:
                return get_cate_for_entity_iterable([entitiy_input],wikipedia_caller,wikidata_caller)
            elif input_type == dict:
                raise TypeError("unsupported type %s" %(input_type) )
            else:
                return get_cate_for_entity_iterable(entitiy_input,wikipedia_caller,wikidata_caller)

        else:
            raise TypeError("unsupported type %s" %(input_type) )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args=parser.parse_args()

if __name__=="__main__":
    main()

