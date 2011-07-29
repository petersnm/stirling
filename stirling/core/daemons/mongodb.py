import logging
import pymongo
import sys
from pymongo import Connection

import stirling

class MongoDB:
    def __init__(self):
        self.database = Connection().stirling
        self.log = logging.getLogger(self.__module__)

    def getEntity(self, _id):
        if _id in self.database.entities.keys():
            return self.database.entities[_id]
        else:
            matches = self.database.entities.find({'_id': _id})
            if matches.count() > 1:
                self.log.error('Too many ID matches!')
                return False
            if matches.count() == 1:
                return self.database.entities[_id]
            else:
                return False

    def searchEntities(self, path):
        if path.count('.') == 0:
            return False
        _module, _class = path.rsplit('.', 1)
        matches         = self.database.entities.find({'_module': _module, '_class': _class})
        ret_list        = []
        if matches:
            for match in matches:
                if match['_id'] in matches:
                    ret_list.append(matches[match]['_id'])
                else:
                    try:
                        __import__(match['_module'])
                        mod = sys.modules[match]['_module']
                    except:
                        continue
                    try:
                        match = getattr(mod, match['_class'])(from_dict=match, from_db=True)
                    except:
                        continue
                    matches[match._id] = match
                    ret_list.append[match]
            if ret_list: return ret_list
            else:        return False
        else:
            return False

    def cloneEntity(self, path, *args, **kwargs):
        if path.count('.') == 0:
            print('path.count(\'.\') == 0')
            return False
        _module, _class = path.rsplit('.',1)
        try:
            __import__(_module)
            mod = sys.modules[_module]
        except:
            print('import failed')
            return False
        try:
            entity = getattr(mod, _class)(*args, **kwargs)
        except:
            print('setting entity failed')
            return False
        clone = entity()
        self.database.entities[clone._id] = clone
        return clone
