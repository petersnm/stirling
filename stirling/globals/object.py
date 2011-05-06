import logging
logging.getLogger(__name__)
logging.debug("Imported")

import sys
from pymongo.objectid import ObjectId
from stirling.daemon.database import MongoDB

objects = {}

def get(_id):
    if _id in objects.keys():
        return objects[_id]
    else:
        objs = MongoDB.objects.find({'_id': _id})
        if objs.count() == 1:
            objects[_id] = objs[0]
            return objects[_id]
        else:
            return False

def search(path):
    if path.count('.') == 0:
        return False
    _module, _class = path.rsplit('.', 1)
    objs = MongoDB.objects.find({'_module': _module, '_class': _class})
    ret_list = []
    if objs:
        for obj in objs:
            try:
                __import__(obj['_module'])
                mod = sys.modules[obj['_module']]
            except:
                logging.debug("failed to import '%s'" % (obj['_module'],))
                continue
            try:
                obj = getattr(mod, obj['_class'])(from_dict=obj,
                        from_db=True)
            except:
                logging.debug("failed to init '%s'" % (obj['_class'],))
                continue
            objects[obj._id] = obj
            ret_list.append(obj)
        if ret_list: return ret_list
        else: return False
    else:
        return False

def clone(path, *args, **kwargs):
    if path.count('.') == 0:
        return False
    _module, _class = path.rsplit('.', 1)
    try:
        __import__(_module)
        mod = sys.modules[_module]
    except:
        # log an error importing it
        return False
    try:
        obj = getattr(mod, _class)(*args, **kwargs)
    except:
        # log teh error
        return False
    objects[obj._id] = obj
    return obj

