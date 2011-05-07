"""
The master object of the MUD, all objects inherit it at some point
"""

# This will have to be replaced by
import logging
logging.basicConfig(level=logging.DEBUG)
from pymongo.objectid import ObjectId

import stirling
from stirling.daemon.database import MongoDB, Properties

class MasterObject(object):
    '''MasterObject(object) is the base object, from which the majority of 
    daemons and in-game objects are subclassed. '''
    def __init__(self, from_dict={}, from_db=False):
        self.__dict__['exclude'] = ['properties', 'logger', 'debug', 'info', 
          'warning', 'error',  'save', 'move', 'remove', 'add_inventory', 
          'tell',]
        self.__dict__['properties'] = Properties(self, 
          from_dict, from_db=from_db)
        # Initialize the object's logging
        self.logger = logging.getLogger(self.__module__)
        

    def new(self):
        ''' Set the default properties of every object. '''
        self.name = str(self._id)
        self.desc = 'this is a thing'
        self.nametags = Nametags(['object','thing'])
        self.inventory = []

    def save(self):
        ''' Force a save of the object. '''
        self.properties.save()


    def __setattr__(self, attr, value):
        ''' Unless specifically exempted, adds attr to the properties dict 
        with a value of value. '''
        if attr in self.exclude:
            self.__dict__[attr] = value
        else:
            self.__dict__['properties'][attr] = value

    def __getattr__(self, attr):
        ''' Unless attr is in self.exclude, query the properties doct for it 
        and return its' value. '''
        if attr in self.exclude:
            # due to the way __getattr__ works, this should never be called,
            # keeping it here just in case someone does something silly.
            return self.__dict__[attr]
        else:
            return self.__dict__['properties'][attr]

    def __delattr__(self, attr):
        ''' Remove the attribute. '''
        if attr in self.exclude:
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
            destination.add_inventory(self)
            self.environment = destination._id
            return True
        elif isinstance(destination, ObjectId) == True:
            stirling.get(destination).add_inventory(self)
            self.environment = destination._id
            return True
        else:
            return False

    def add_inventory(self, item):
        if isinstance(item, MasterObject) == True:
            self.properties['inventory'].append(item._id)
            return
    


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


    @property
    def name(self):
        ''' An object's name is its proper name.  For example, a sailor named 
        Pete might have a name of 'Salty Pete', or a baker might have a name 
        of 'skilled baker'. '''
        return self.properties['name']

    @name.setter
    def name(self, value):
        ''' When an object's name is changed, it should also remove the 
        previous name from the nametags, and replace it with the new 
        one. '''
        if isinstance(value, str): 
            try:
                self.nametags.remove(self.properties['name'])
            except:
                pass
            self.nametags.append(value.lower())
            self.properties['name'] = value
            self.debug('set name to '+value)
        else:
            self.warning('name setter passed incorrect type; expecting string')

    @property
    def environment(self):
        ''' The environment is stored as an _id, so we have to use 
        stirling.get() to retrieve the object referred to. '''
        return stirling.get(self.__dict__['properties']['environment'])

    @property
    def nametags(self):
        return self.properties['nametags']

    #def add_nametag(self, tag):
    #    if isinstance(tag, str):
    #        try:
    #            if self.properties['nametags'].count(tag) is 0:
    #                self.properties['nametags'].append(tag)
    #        except KeyError:
    #            self.properties['nametags'] = [tag]
    #    else:
    #        self.warning('add_nametag() was expecting string')


class Nametags(list):
    def __init__(self, obj, _list=[]):
        list.__init__(self, _list)

    def append(self, item):
        if isinstance(item, str):
            try:
                if self.properties['nametags'].count(tag) is 0:                
                    list.append(self, item)
            except:
                pass
        else:
            pass
    


class Inventory(list):
    def __init__(self, parent, _list=[], from_db=False):
        list.__init__(self, _list)
        self.parent = parent
        

    def search(self, nametag):
        L = []
        for obj_id in self:
            obj = objects.get(obj_id)
            if nametag in obj.nametags:
                L.append(obj_id)
        return L
