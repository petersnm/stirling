"""
The master object of the MUD, all objects inherit it at some point
"""

# This will have to be replaced by
import logging
logging.basicConfig(level=logging.DEBUG)
from pymongo.objectid import ObjectId
import sys

import stirling
from stirling.daemon.database import MongoDB
from stirling.globals.object import objects

class MasterObject(object):
    '''MasterObject(object) is the base object, from which the majority of 
    daemons and in-game objects are subclassed. '''
    def __init__(self, from_dict={}, from_db=False):
        self.__dict__['exclude'] = ['properties', 'logger', 'debug', 'info', 
          'warning', 'error',  'save', 'move', 'remove', 'tell',
          '_get_environment', '_set_name']
        self.__dict__['customs'] = ['name']
        self.logger = logging.getLogger(self.__module__)
        self.__dict__['properties'] = Properties(self, 
          from_dict, from_db=from_db)
        # Initialize the object's logging
        

    def new(self):
        ''' Set the default properties of every object. '''
        self.nametags = NameTags(self, ['object','thing'])
        self.name = str(self._id)
        self.desc = 'this is a thing'
        self.inventory = Inventory(self)

    def save(self):
        ''' Force a save of the object. '''
        self.properties.save()


    def __setattr__(self, attr, value):
        ''' Unless specifically exempted, adds attr to the properties dict 
        with a value of value. '''
        if "_set_%s" % (attr,) in dir(self):
            print("tryna call _set_")
            return object.__getattribute__(self, "_set_%s" % (attr,))(value)
        elif attr in self.exclude or attr in self.__dict__:
            self.__dict__[attr] = value
        else:
            self.__dict__['properties'][attr] = value
            self.save()

    def __getattr__(self, attr):
        ''' Unless attr is in self.exclude, query the properties doct for it 
        and return its' value. '''
        if not (attr.startswith('_get_') or attr.startswith('_set_')) and\
           '_get_%s' % (attr,) in dir(self):
            return object.__getattribute__(self, '_get_%s' % (attr,))() 
        elif attr in self.exclude:
            # due to the way __getattr__ works, this should never be called,
            # keeping it here just in case someone does something silly.
            return self.__dict__[attr]
        else:
            return self.__dict__['properties'][attr]

    def __delattr__(self, attr):
        ''' Remove the attribute. '''
        if hasattr(self, "_del_%s" % (attr,)) and not attr.startswith('_del_'):
            return getattr(self, "_del_%s" % (attr,))
        elif attr in self.exclude:
            # why are you deleting something that's in .exclude, they're mostly
            # core functions. do we want to disallow this?
            # yes -- emsenn
            del self.__dict__[attr]
        else:
            del self.properties[attr]


    def tell(self, message):
        if isinstance(message, str):
            pass
        pass


    # Move and remove
    def move(self, destination):
        # move the object from one environment to another
        if isinstance(destination, MasterObject) == True:
            destination.inventory.append(self._id)
            self.environment = destination._id
            return True
        elif isinstance(destination, ObjectId) == True:
            stirling.get(destination).inventory.append(self._id)
            self.environment = destination._id
            return True
        else:
            return False

    def remove(self):
        try:
            self.environment.inventory.remove(self._id)
        except:
            pass

    def destroy(self):
        self.remove()
        MongoDB.objects.remove(self._id)

    # These need to be replaced once we have a logging daemon
    def debug(self, message):
        self.logger.debug(message)
        return
    def info(self, message):
        self.logger.info(message)
        return
    def warning(self, message):
        self.logger.warning(message)
        self.tell('You have caused a minor error.  Please report:\n'+message)
        return
    def error(self, message):
        self.logger.error(message)
        self.tell('++ERROR++ Please report the following:\n'+message) 
        return


    def _set_name(self, value):
        ''' When an object's name is changed, it should also remove the 
        previous name from the nametags, and replace it with the new 
        one. '''
        self.debug('set name to '+value)
        if isinstance(value, str): 
            try:
                self.nametags.remove(self.properties['name'])
            except:
                self.debug(sys.exc_info())
            self.nametags += [value.lower()]
            self.properties['name'] = value
        else:
            self.warning('name setter passed incorrect type; expecting string')

    def _get_environment(self):
        ''' The environment is stored as an _id, so we have to use 
        stirling.get() to retrieve the object referred to. '''
        return stirling.get(self.__dict__['properties']['environment'])


class AutoSaveList(list):
    def __init__(self, parent, _list=[]):
        list.__init__(self, _list)
        self.parent = parent

    def append(self, item):
        self.parent.debug(self)
        self += [item]
        self.parent.debug(self)
        self.parent.save()
        self.parent.debug(self)

    def remove(self, item):
        x = list.remove(self, item)
        self.parent.save()
        return x

    def insert(self, index, item):
        x = list.insert(self, index, item)
        self.parent.save()
        return x 

    def pop(self, index=-1):
        x = list.pop(self, index)
        self.parent.save()
        return x

class NameTags(AutoSaveList):
    def __init__(self, parent, _list=[]):
        list.__init__(self, _list)
        self.parent = parent

    def append(self, item):
        if isinstance(item, str):
            try:
                if self.parent.properties['nametags'].count(tag) is 0:                
                    AutoSaveList.append(self, item)
            except:
                pass


class Inventory(AutoSaveList):
    def __init__(self, parent, _list=[], from_db=False):
        list.__init__(self, _list)
        self.parent = parent

    def contents(self):
        foo = []
        for item in self:
            foo.append(stirling.get(item))
        return foo
 
    def search(self, nametag):
        L = []
        for obj_id in self:
            obj = objects.get(obj_id)
            if nametag in obj.nametags:
                L.append(obj_id)
        return L

class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        # this is becasue if it's from the DB, we dont' need to fill the db, but if it isn't, we do.
        if not from_db:
            self['special'] = {
                    'inventory': 'Inventory',
                    'nametags': 'NameTags',
            }
            self['_id'] = MongoDB.objects.insert(self)
            parent.__dict__['_id'] = self['_id']
            self['_class'] = parent.__class__.__name__
            self['_module'] = parent.__class__.__module__
            objects[self['_id']] = parent
        try:
            for key, cls in self['special'].items():
                if key in self and not isinstance(self[key], globals()[cls]):
                    self[key] = globals()[cls](parent, self[key])
                    parent.debug((parent, self[key]))
        except:
            parent.debug(sys.exc_info())

    def __setitem__(self, item, value):
        wat = dict.__setitem__(self, item, value)
        try:
            MongoDB.objects.save(self)
        except Exception:
            logging.debug(sys.exc_info())
        return wat

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        wat = dict.__delitem__(item)
        MongoDB.objects.save(self)
        return wat

    def save(self):
        MongoDB.objects.save(self)



