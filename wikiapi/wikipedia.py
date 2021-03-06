"""
get data from Wikipedia api
"""

from wikibase import *

class Wikipedia(Wikibase):
    """
    Wikipedia class
    """

    def __init__(self):
        self._END_POINT="https://www.Wikipedia.org/w/api.php?"



    def get_entity_name(self,title,limit = None):
        print "for name %s" %title
        params = self.get_default_configuration()
        params['action'] = 'opensearch'
        params['search'] = title
        params['namespace'] = 0
        params['redirects'] = 'resolve'
        if limit:
            params['limit'] = limit
        content =  self.call_api(params)
        try:
            result = json.loads(content)            
        except ValueError:
            raise ResultErrorException(content,"mal-formatted")
        else:
            try:
                entity_name = result[1][0]
            except IndexError:
                raise ResultErrorException(content,"unexpected result structure")
            else:
                print "found entity %s" %entity_name
                return entity_name






def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("")
    args=parser.parse_args()

if __name__=="__main__":
    main()

