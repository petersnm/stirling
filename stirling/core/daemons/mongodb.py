"""
    .. module:: stirling.core.daemons.mongodb
        :synopsis: This daemon acts as a layer between Stirling and the 
            external MongoDB daemon.
    .. modauthor::  Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1 import logging
"""
import logging
import pymongo
import sys
from pymongo import Connection

import stirling

class MongoDB:
    """ Contains the functions used to interact with the external database.  
    """
    def __init__(self):
        """ Creates a layer between Stirling and the external MongoDB daemon.  

            :var database: external MongoDB database ``stirling``
            :var clones: dict of MongoDB collection ``clones`` in the 
                ``stirling`` database
            :var loaded_clones: dict of objects already loaded from `clones`
            :returns: None

            .. note:: `clones` is a dict representing the ``clones`` 
                collection within MongoDB's ``stirling`` database, whereas 
                `loaded_clones` is a dict of **only the currently 
                loaded clones**.

            Attempts to connect to the external MongoDB daemon's database 
            ``stirling``, before loading a dict of both clones and user 
            properties from the external MongoDB database ``stirling``.

            .. todo:: These docstrings mention user properties a few times; 
                users don't exist.
        """
        self.database = Connection().stirling
        self.clones = self.database.clones
        self.loaded_clones = {}
        self.users = self.database.users
        self.loaded_users = {}
        self.log = logging.getLogger(self.__module__)

    def get_clone(self, _id):
        """ Find and return an entity matching `_id`.

            :param _id: A unique identifier for the clone
            :type _id: str
            :rtype: object or None
            :returns: an object cooresponding to the clone with an 
                ``_id`` equal to `_id`
 
            First checks `loaded_clones` to see if there is a 
            match for `_id` among the clones alreadiy loaded, and if so, 
            returns the matching object.  If the entity is not already loaded, 
            getEntity attempts to find the object with the proper `_id` in 
            `clones`.  If there is a match, add it to 
            `loaded_clones` and return it.
        """
        if _id in self.loaded_clones.keys():
            return self.loaded_clones[_id]
        else:
            matches = self.clones.find({'_id': _id})
            if matches.count() > 1:
                self.log.warning('Too many ID matches!')
                return None
            if matches.count() == 1:
                self.loaded_clones[_id] = self.clones[_id]
                return self.clones[_id]
            else:
                return None

    def search_clones(self, path):
        """ Search for all clones matching `path`

            :param path: full path to the entity class you wish to find, i.e. 
                ``stirling.modules.entities.obj.artificial.Toothpick``
            :type path: str
            :rtype: list or None
            :returns: all clones which match `path`

            `path` is split to refer to the module and class separately, which 
            are both then used to search `clones` for a match.  The generated 
            list of matches is then checked to make sure it is a valid entity, 
            all unloaded clones which match are loaded, and the list is returned. 
         """
        if path.count('.') == 0:
            return None
        _module, _class = path.rsplit('.', 1)
        matches         = self.clones.find({'_module': _module, '_class': _class})
        ret_list        = []
        if matches:
            for match in matches:
                if match['_id'] in self.loaded_clones:
                    ret_list.append(self.loaded_clones['_id'])
                else:
                    try:
                        __import__(match['_module'])
                        mod = sys.modules[match]['_module']
                    except:
                        self.log.warning('Unable to import specified module')
                        return None
                    try:
                        match = getattr(mod, match['_class'])(from_dict=match, from_db=True)
                    except:
                        self.log.warning('Unable to clone matching entity')
                        return None
                    self.loaded_clones[match._id] = match
                    ret_list.append[match]
            if ret_list:
                return ret_list
            else:
                return False
        else:
            return False

    def clone_entity(self, path, *args, **kwargs):
        """ Creates a clone of the class specified by `path`

            :param path: full path to the entity class you want to clone, i.e.
                ``stirling.modules.entities.living.Homo_Sapien``
            :type path: str
            :param \*args: arguments passed to the cloned entity
            :param \*\*kwargs: keyword arguments passed to the cloned entity
            :rtype: object or None
            :returns: clone of the class at `path`

            Creates a new clone of the class specified by `path`, passing to 
            it all `*args` and `**kwargs`, before returning the new clone.
        """
        if path.count('.') == 0:
            self.log.debug('path count = 0')
            return None
        _module, _class = path.rsplit('.', 1)
        try:
            __import__(_module)
            mod = sys.modules[_module]
        except:
            self.log.debug('import failed')
            return None
        try:
            clone = getattr(mod, _class)(*args, **kwargs)
        except:
            self.log.debug('creating clone failed')
            return None
        clone.save()
        self.loaded_clones[clone._id] = clone
        return clone

    def get_user(self, name):
        match = self.users.find_one({ "username" : name })
        if type(match) is not dict:
            self.log.warning('Attempted to load nonexisting user %s' % (name))
            return False
        else:
            return match

    def make_user(self, name, password):
        self.users.insert({ 'username' : name, 'password' : password})
        return True

class persistList(list):
    def __init__(self, parent, _list=[]):
        list.__init__(self, _list)
        self.parent = parent

    def append(self, item):
        self += [item]
        self.parent.save()

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


class PersistDict(dict):
    def __init__(self, parent, _dict={}):
        dict.__init__(self, _dict)
        self.parent = parent

    def __setitem__(self, item):
        dict.__setitem__(self, item)
        self.parent.save()
    
    def __delitem__(self, item):
        dict.__delitem__(self, item)
        self.parent.save()
