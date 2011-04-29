"""
/lib/std/object.py
abzde@Stirling
280411 emsenn@Stirling

The master object of the MUD, all objects inherit it at some point
"""

import logging
logging.basicConfig(level=logging.DEBUG)

class MasterObject:
    def __init__(self):
        self.properties = {
                'name': 'object',
                'nametags': ['object'],
                'desc': 'this is a thing.',
                'inventory': [],
        } 
        # dev not for emsenn:
        #   please give /all/ of those setters, I'm doing it this way for 
        #   database stuff, it'll make it much easier.
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

    @property
    def nametags(self):
        return self.properties['nametags']

    @nametags.setter
    def nametags(self, tags):
        if isinstance(tags, list):
            for tag in tags:
                add_nametag(tag)
        else:
            self.warning('nametag setter passed incorrec type; expecting list')

    @nametags.deleter
    def nametags(self, tag):
        if isinstance(tag, str):
            if self.properties['nametags'].count(tag) > 0:
                self.properties['nametags'].remove(tag)

    def add_nametag(self, tag):
        if isinstance(tag, str):
            if self.properties['nametags'].count(tag) is 0:
                self.properties['nametags'].append(tag)
        else:
            self.warning('add_nametag() was expecting string')


    @property
    def name(self):
        return self.properties['name']

    @name.setter
    def name(self, name):
        # basestring is the parent of str and unicode
        if isinstance(name, str): 
            self.nametags.remove(self.properties['name'])
            self.add_nametag(name.lower())
            self.properties['name'] = name
        else:
            self.warning('name setter passed incorrect type; expecting string')

    # @name.deleter
    # def name(self):
    #     del self.properties['name']
    # I can't think of any good reason that we would want to delete names, but
    # here's the syntax if we /do/ need to.

    # def set_name(self, name):
    #     ''' set_name(name)
    #         Sets the object's name to string 'name'.  An object's name acts as 
    #         its main displayed identity.  For example, a man named Fat Sally 
    #         might use set_name('Fat Sally')
    #     '''
    #     if isinstance(name, str):
    #         self.rm_nametag(self.name)
    #         self.add_nametag(name.lower())
    #         self.name = name
    #     else:
    #         self.warning('set_name() passed incorrect type; expecting string')
    #     return

    def set_desc(self, desc):
        if isinstance(desc, str):
            self.desc = desc

    # Move and remove
    def move(self, destination):
        # move the object from one environment to another
        if isinstance(destination, MasterObject) == True:
            destination.add_inventory(self)
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
