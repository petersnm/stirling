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
    daemons and in-game objects are subclassed.'''
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

    def __setattr__(self, attr, value):
        if attr in self.exclude:
            self.__dict__[attr] = value
        else:
            # These are if checks to try and filter out special variables
            # It should be rewritten to iterate through a list for special 
            # variables and run their setters, so that things that inherit
            # MasterObject can add in other special properties.
            if attr == 'name':
                if isinstance(value, str): 
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
            if attr == 'environment':
                return stirling.get(self.__dict__['properties']['environment'])
            return self.__dict__['properties'][attr]

    def __delattr__(self, attr):
        if attr in self.exclude:
            # why are you deleting something that's in .exclude, they're mostly
            # core functions. do we want to disallow this?
            # yes -- emsenn
            del self.__dict__[attr]
        else:
            del self.properties[attr]

    def save(self):
        self.properties.save()

    def add_nametag(self, tag):
        if isinstance(tag, str):
            if self.properties['nametags'].count(tag) is 0:
                self.properties['nametags'].append(tag)
        else:
            self.warning('add_nametag() was expecting string')

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
    
    def remove(self):
        # remove the object from the game
        return
    

    # This is a very simplistic way of doing inventories.  When we add in 
    # doing everything in memory via a database, this will change lots.  Oh boy!
    def add_inventory(self, item):
        if isinstance(item, MasterObject) == True:
            self.properties['inventory'].append(item)
            return
    

    def tell(self, message):
        if isinstance(message, str):
            pass
        pass


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
