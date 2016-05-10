from wikipedia import Wikipedia
from wikidata import Wikidata
import wikiexceptions 
import time
from collections import Iterable


class WikiCategory(object):
    """
    the class used to find categories for entities
    """
    def  __init__():
        self.wikipedia_caller = Wikipedia()
        self.wikidata_caller = Wikidata()
        self._cate_info = {}




    def _get_single_entity_cate(self,entity):
        """
        find the category info for a single entity

        Updates
        -----------------------------------------
        cate_info: a dict categories of the entities

                    key: entity name
                    value: a list of categories of the key

        """

        if entity in self._cate_info:
            return
        else:
            self._cate_info[entity] = []
        try:
            entity_name = self.wikipedia_caller.get_entity_name(entity)
        except wikiexceptions.ResultErrorException:
            print "cannot find an entity for name %s" %entity
            self._cate_info[entity] = None
        try:
            entity_info = self.wikidata_caller.get_entity_info_by_name(entity_name)
        except wikiexceptions.NoClassException:
            print "entity %s has no class info" %entity_name
            self._cate_info[entity] = None

        else:
            for cid in entity_info['class_info']:
                self._cate_info[entity].append(entity_info['class_info'])


    def _get_cate_for_entity_iterable(self,entity_iterable):
        """
        find the categories info for an Iterable of entities

        Updates
        -----------------------------------------
        cate_info: a dict categories of the entities

                    key: entity name
                    value: a list of categories of the key

        """

        for entity in entity_iterable:
            result =  _get_single_entity_cate(entity)
            time.sleep(5)

    
    def get_cates(self,entitiy_input):
        """
        Find the categories info for entities. Do type check
        first and support both string and Iterable(except dict)
        input 

        Updates:
        -----------------------------------------
        cate_info: a dict categories of the entities

                    key: entity name
                    value: a list of categories of the key

        """
        input_type = type(entitiy_input)
        if isinstance(entitiy_input,Iterable):
            if type(entitiy_input) == str:
                self._get_single_entity_cate(entity)
            elif input_type == dict:
                raise TypeError("unsupported type %s" %(input_type) )
            else:
                self._get_cate_for_entity_iterable(entitiy_input)

        else:
            raise TypeError("unsupported type %s" %(input_type) )


    @property
    def cate_info(self):
        return self._cate_info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",nargs='+')
    args=parser.parse_args()
    category_finder = WikiCategory()
    category_finder.get_cates(args.input)
    print category_finder.cate_info

if __name__=="__main__":
    main()
