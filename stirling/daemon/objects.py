import logging
logging.getLogger(__name__)
logging.debug("Imported")

import sys
from pymongo.objectid import ObjectId
from stirling.obj.spec.daemon import Daemon
from stirling.daemon.database.mongo import database

objects = {}

class Memory():
    def __init__():
        pass
        #super(Memory, self).__init__()


class NoSuchItemError(LookupError):
    pass

def load_object(to_load, args=[]):
    if isinstance(to_load, ObjectId):
        objs = database.objects.find({'_module': _module, '_class': _class})
        if objs.count() == 0:
            logging.warning('load_objects recieved invalid ObjectId')
            return False
        elif objs.count() == 1:
            obj_dict = objs[0]
        else:
            logging.warning('load_objects got multiple objects with that path')
            return False
        _module = obj_dict['_module']
        _class = obj_dict['_class']
        from_db = True
    elif isinstance(to_load, str):
        if '.' in to_load:
            _module, _class = to_load.rsplit('.', 1)
        else:
            logging.warning('load_object recieved invalid path')
            return False
        objs = database.objects.find({'_module': _module, '_class': _class})
        if objs.count() == 0:
            obj_dict = {}
            from_db = False
        elif objs.count() == 1:
            obj_dict = objs[0]
            from_db=True
        else:
            logging.warning('load_objects got multiple objects with that path')
            return False
    else:
        
        logging.warning('load_object recieved invalid arg, expected type'
                       'ObjectId or str')
    try:
        __import__(_module)
        imported = sys.modules[_module]
    except ImportError:
        logging.warning('load_object tried to load invalid module')
        return False
    except:
        pass
    if hasattr(imported, _class):
            obj = getattr(imported, _class)(from_dict=obj_dict, from_db=from_db)
            objects[obj._id] = obj
            return obj._id
    else:
        logging.warning('load_obj tried to load a nonexistent class')
        return False
        

def get_object(_id):
    if _id in objects.keys():
        return objects[_id]
    else:
        raise NoSuchItemError('no such item with id "%s"' % (_id,))
