import json

class Movedex:

    def __init__(self, dex_file):
        self.dex = json.load(open(dex_file))
    
    def search_by_name(self, name):
        result_list = []
        for key in self.dex.keys():
            if name.lower() in self.dex[key]['name'].lower():
                result_list.append((key, self.dex[key]))
        return result_list

