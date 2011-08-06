"""
    .. module:: stirling.core.daemons.mongodb

    .. moduleauthor:: Hunter Carroll <abzde@abzde.com>
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    The :mod:`mongodb <stirling.core.daemons.mongodb>` module contains the 
    :class:`MongoDB() <stirling.core.daemons.mongodb.MongoDB>`, as well as 
    modified datatypes :class:`persistList() 
    <stirling.core.daemons.mongodb.persistList>` and :class:`persistDict() 
    <stirling.core.daemons.mongodb.persistDict>`, which interact with `MongoDB`.
"""
import sys
from pymongo import Connection

import stirling

class MongoDB(stirling.core.BaseObj):
    """ Contains the functions used to interact with the external database.  
    """
    def __init__(self):
        """ Creates a layer between Stirling and the external MongoDB daemon.  

            .. versionadded:: 0.1

            :var    database:       external MongoDB database ``stirling``
            :var    clones:         All cloned entities, loaded and unloaded
            :var    loaded_clones:  Only currently-loaded clones
            :var    users:          All users.

            :returns:               None

            .. note:: The bootstrapper will create an instance of this daemon 
                upon boot which may be referred to by ``stirling.mDB``.

            
        """
        super(MongoDB, self).__init__()
        self.database = Connection().stirling
        self.clones = self.database.clones
        self.loaded_clones = {}
        self.users = self.database.users


    def get_clone(self, ent_id):
        """ Find and return an entity matching `ent_id`.

            .. versionadded:: 0.1

            :param  ent_id:    A unique identifier for the clone
            :type   ent_id:    str

            :returns:       object of entity matching `ent_id` or None
 
            First checking `self.loaded_clones` then `self.clones`, 
            `get_clone()` returns either the object that matches the 
            provided ID, or None.
        """
        if ent_id in self.loaded_clones.keys():
            return self.loaded_clones[ent_id]
        else:
            matches = self.clones.find({'ent_id': ent_id})
            if matches.count() > 1:
                self.warning('Too many ID matches!')
                return None
            if matches.count() == 1:
                path = "%s.%s" % (matches[0]['_module'], matches[0]['_class'])
                obj = self.clone_entity(path, from_dict=matches[0])
                self.loaded_clones[ent_id] = obj 
                return obj
            else:
                return None


    def search_clones(self, path):
        """ Search for all clones matching `path`.

            .. versionadded: 0.1

            :param  path:   full path to the entity class you wish to find, i.e. 
                                ``world.misc.entity.obj.Toothpick``
            :type   path:   str
            
            :returns: list of all objects cloned from the class ``path`` (or 
                None)

            `search_clones()` first looks for all loaded clones which are 
            instanced from `path`, and then all remaining clones, before 
            returning a list of all matches.

            .. todo:: The try/except of ``match = getaattr(...)`` in 
                `MongoDB().search_clones()` doesn't specify exception type.
         """
        if path.count('.') == 0:
            return None
        _module, _class = path.rsplit('.', 1)
        matches         = self.clones.find({'_module': _module, 
                                           '_class': _class})
        ret_list        = []
        if matches:
            for match in matches:
                if match['ent_id'] in self.loaded_clones:
                    ret_list.append(self.loaded_clones['ent_id'])
                else:
                    try:
                        __import__(match['_module'])
                        mod = sys.modules[match]['_module']
                    except ImportError:
                        self.warning('Unable to import specified module')
                        return None
                    try:
                        match = getattr(mod, match['_class'])(from_dict=match,
                           from_db=True)
                    except:
                        self.warning('Unable to clone matching entity')
                        return None
                    self.loaded_clones[match.ent_id] = match
                    ret_list.append[match]
            if ret_list:
                return ret_list
            else:
                return False
        else:
            return False

    def clone_entity(self, path, *args, **kwargs):
        """ Creates a clone of the class specified by `path`

            .. versionadded: 0.1

            :param  path:       full path to the entity class you want to 
                                clone, i.e. 
                                ``stirling.modules.entities.living.homoSapien``
            :type   path:       str

            :param  \*args:     arguments passed to the cloned entity
            :type   \*args:     mixed

            :param  \*\*kwargs: keyword arguments passed to the cloned entity
            :type   \*\*kwargs: mixed

            :returns: object of the new clone of the class at `path` (or None)

            Creates a new clone of the class specified by `path`, passing to 
            it all `*args` and `**kwargs`, before returning the new clone.

            .. todo:: The try/except of ``match = getaattr(...)`` in 
                `MongoDB().clone_entity()` doesn't specify exception type.
        """
        if path.count('.') == 0:
            self.debug('te;ifjasd')
            return None
        _module, _class = path.rsplit('.', 1)
        try:
            __import__(_module)
            mod = sys.modules[_module]
        except ImportError:
            self.debug('import of module failed')
            return None
        try:
            clone = getattr(mod, _class)(*args, **kwargs)
        except:
            self.debug('instancing of class failed')
            return None
        clone.save()
        self.loaded_clones[clone.ent_id] = clone
        return clone

    def get_user(self, name):
        """ Returns the user with username `name`

            .. versionadded: 0.1

            :param  name:   The username of the account you want to access.
            :type   name:   str

            :return:        A dict of the matching user (or None).

            `get_user()` returns a dict of the user profile matching `name`, 
            or None.  Simple as that.
        """
        match = self.users.find_one({ "username" : name })
        if type(match) is not dict:
            self.warning('Attempted to load nonexisting user %s' % (name))
            return False
        else:
            return match

    def make_user(self, name, password, ent_id, birthtime):
        """ Creates a new user

            .. versionadded:: 0.1

            :param  name:       The username you wish to register.
            :type   name:       str

            :param  password:   The desired password.
            :type   password:   hexdigest

            :return:            True or False

            This registers user `name` with a password hash of `password`.
            
            .. todo:: Expand make_user() to either use multiple submethods or
                return better errors.  Oh, and have error checking.
            .. todo:: Add more user properties like creation time, age, and so 
                on.
        """
        self.users.insert({'username' : name, 'password'  : password, 
                           'ent_id' : ent_id, 'birthtime' : birthtime,})
        return True

class PersistList(list):
    """ Custom datatype for persistent lists
    """
    def __init__(self, parent, _list):
        """ Create a new peristent list.

            .. versionadded:: 0.1

            :param  parent: The object within which the list is stored.
            :type   parent: object

            :param  _list:  The list to be created.
            :type   _list:  list

            :return:       None

            `persistList()` creates a new list matching `_list` within 
            `parent`.

            .. warning:: `parent` must be an :term:`entity`.
        """
        list.__init__(self, _list)
        self.parent = parent
        return

    def append(self, item):
        """ Append a new item to the list

            .. versionadded:: 0.1

            :param  item:   the item to be added
            :type   item:   mixed

            :return:       None

            Append a new item the list and save the parent entity.
        """
        self += [item]
        self.parent.save()
        return

    def remove(self, item):
        """ Remove an item from the list

            .. versionadded:: 0.1

            :param  item:   the item to remove
            :type   item:   mixed

            :return:        None or error

            Removes `item` from the list and saves the parent.
        """
        result = list.remove(self, item)
        self.parent.save()
        return result

    def insert(self, index, item):
        """ Insert `item` at position `index`

            .. versionadded: 0.1

            :param  index:  The position at which to insert the `item`.
            :type   index:  int

            :param  item:   The item to insert to the list.
            :tyep   item:   mixed

            :return:        None or error

            Inserts `item` in the list, at position `index`, and saves the 
            parent.
        """
        result = list.insert(self, index, item)
        self.parent.save()
        return result

    def pop(self, index=-1):
        """ Insert `item` at position `index`

            .. versionadded: 0.1

            :param  index:  The index of the desired item from the list.
            :type   index:  int

            :return:        None or error

            Pops the value at `index` out of the array.
        """
        result = list.pop(self, index)
        self.parent.save()
        return result    


class PersistDict(dict):
    """ Custom dict datatype for persistence.
    """
    def __init__(self, parent, _dict):
        """ Initialize a custom dict.

            .. versionadded:: 0.1

            :param  parent: The object within which the dict is stored.
            :type   parent: object

            :param  _dict:  The list to be created.
            :type   _dict:  dict

            :return:       None

            `persistDict()` creates a new dict matching `_dict` within 
            `parent`.

            .. warning:: `parent` must be an :term:`entity`.
        """
        dict.__init__(self, _dict)
        self.parent = parent

    def __setitem__(self, item):
        dict.__setitem__(self, item)
        self.parent.save()
    
    def __delitem__(self, item):
        dict.__delitem__(self, item)
        self.parent.save()
