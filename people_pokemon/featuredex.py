import json

class Featuredex:

    data = None
    
    @classmethod
    def _jit_load(cls, dex_file='./people_pokemon/featuredex.json'):
        if cls.data == None:
            cls.data = json.load(open(dex_file))
    
    @classmethod
    def get_by_key(cls, key):
        cls._jit_load()
        return cls.data[key]

    @classmethod
    def search_by_name(cls, name):
        '''Returns a list of tuple-pairs, where the first entry in the list is the first match found in the featuredex for the name. The tuple has the data dictionary key as the first entry, and the data itself as the second'''
        cls._jit_load()
        result_list = []
        for key in cls.data.keys():
            if name.lower() in cls.data[key]['name'].lower():
                result_list.append((key, cls.data[key]))
        return result_list

