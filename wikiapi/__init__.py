
from wikipedia import Wikipedia
from wikidata import Wikidata
import wikiexceptions 
from collections import Iterable

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


__all__ = ['Wikipedia', 'Wikidata', 'wikiexceptions','get_cates']