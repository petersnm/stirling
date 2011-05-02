"""
/lib/std/object.py
abzde@Stirling
280411 emsenn@Stirling

The master object of the MUD, all objects inherit it at some point
"""

import logging
logging.basicConfig(level=logging.DEBUG)

from stirling.daemon.database import database
from stirling.daemon.objects import objects, load_object, get_object

class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        self.parent = parent
        # this is becasue if it's from the DB, we dont' need to fill the db, but if it isn't, we do.
        if not from_db:
            self['_id'] = database.objects.insert(self)
            self.parent.__dict__['_id'] = self['_id']
            self['_class'] = self.parent.__class__.__name__
            self['_module'] = self.parent.__class__.__module__
            objects[self['_id']] = self.parent

    
    def __setitem__(self, item, value):
        try:
            self.parent.debug('item set '+item+":"+value)
        except:
            pass
        dict.__setitem__(self, item, value)
        database.objects.save(self)

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        dict.__delitem__(item)
        database.objects.save(self)

    def save(self):
        database.objects.save(self)


class Inventory(list):
    def __init__(self, parent, _list=[], from_db=False):
        list.__init__(self, _list)
        self.parent = parent
        
    def search(self, nametag):
        l = []
        for obj_id in self:
            obj = objects.get(obj_id)
            if nametag in obj.nametags:
                l.append(obj_id)
        return l

class MasterObject(object):
    def __init__(self, from_dict={}, from_db=False):
        self.__dict__['exclude'] = ['properties', 'logger', 'debug', 'info', 'warning',
                        'error',  'save', 'move', 'remove', 'add_inventory',
                        'tell',]
        if from_dict:
            self.__dict__['properties'] = Properties(self, from_dict, from_db=from_db)
        else:
            self.__dict__['properties'] = Properties(self, {
                    'name': 'object',
                    'nametags': ['object'],
                    'desc': 'this is a thing.',
                    'inventory': [],
                    'environment': ''
            }, from_db=from_db)
        # Initialize the object's logging
        self.logger = logging.getLogger(self.__module__)
        

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

    def __setattr__(self, attr, value):
        if attr in self.exclude:
            self.__dict__[attr] = value
        else:
            if attr == 'name':
                if isinstance(value, str): 
                    self.debug('fuck the hell')
                    self.debug(self.nametags)
                    self.debug(self.properties['name'])
                    self.nametags.remove(self.properties['name'])
                    self.add_nametag(value.lower())
                    self.properties['name'] = value
                    self.debug("name set")
                else:
                    self.warning('name setter passed incorrect type; expecting string')
            elif attr == 'nametags':
                if isinstance(values, list):
                    for tag in values:
                        add_nametag(tag)
                else:
                    self.warning('nametag setter passed incorrec type; expecting list')
            else:
                self.__dict__['properties'][attr] = value

    def __getattr__(self, attr):
        if attr in self.exclude:
            # due to the way __getattr__ works, this should never be called,
            # keeping it here just in case someone does something silly.
            return self.__dict__[attr]
        else:
            return self.__dict__['properties'][attr]

    def __delattr__(self, attr):
        if attr in self.exclude:
            # why are you deleting something that's in .exclude, they're mostly
            # core functions. do we want to disallow this?
            del self.__dict__[attr]
        else:
            del self.properties[attr]

    def save(self):
        self.properties.save()

#    @nametags.deleter
#    that doesn't work how you think it does emsenn, I'll fix it sometime, but
#    not the thing I'm concerned with ATM.
#    def nametags(self, tag):
#        if isinstance(tag, str):
#            if self.properties['nametags'].count(tag) > 0:
#                self.properties['nametags'].remove(tag)

    def add_nametag(self, tag):
        if isinstance(tag, str):
            if self.properties['nametags'].count(tag) is 0:
                self.properties['nametags'].append(tag)
        else:
            self.warning('add_nametag() was expecting string')

    # Move and remove
    def move(self, destination):
        # move the object from one environment to another
        if isinstance(get_object(destination), MasterObject) == True:
            get_object(destination).add_inventory(self)
            self.environment = destination
        return
    
    def remove(self):
        # remove the object from the game
        return
    

    # This is a very simplistic way of doing inventories.  When we add in 
    # doing everything in memory via a database, this will change lots.  Oh boy!
    def add_inventory(self, item):
        if isinstance(item, MasterObject) == True:
            self.properties['inventory'].append(item)
            return
    
    def inventory(self, item=None):
        if item == None:
            return inventory
        else:
            if self.properties['inventory'].count(item) > 0:
                return True
            else:
                return False
    

    def tell(self, message):
        if isinstance(message, str):
            pass
        pass
