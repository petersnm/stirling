"""
    .. module:: stirling.entities
        :synopsis: Entities are stateful objects
    .. moduleauthor:: Hunter Carroll <abzde@abzde.com>
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1
"""

import stirling
from stirling.base import BaseObj
from stirling.daemons.mongodb import MongoDB, PersistList, PersistDict
from multiverse import life

class Entity(BaseObj):
    """ A stateful object within Stirling
    """
    def __init__(self, from_dict=None, from_db=False, **kw):
        """ Initialize a new entity.

            :param  from_dict:      Applied as a dict of the entity's 
                                        properties upon creation.
            :type   from_dict:      dict

            :param  from_db:        If true, the object is loaded from the 
                                        database.  (That is to say, loaded 
                                        rather a new one created.)
            :type   from_db:        boolean

            :return:                None

            Creates a new entity with the properties in `from_dict`.  For a 
            full explanation of what exactly an entity within Stirling is, 
            check the :term:`glossary entry <entity>`.
        """
        super(Entity, self).__init__(**kw)
        self.__dict__['exclude'] = ['properties', 'logger', 'debug', 'info',
          'warning', 'error', 'save', 'move', 'remove', 'tell',
          '_get_environment', 'set_name']
        self.__dict__['customs']       = ['name']
        self.__dict__['properties']    = Properties(self, from_dict, 
                                                    from_db=from_db)
        self.nametags   = NameTags(self, ['entity'])
        self.name       = 'Entity'
        self.desc       = 'This is an entity.'
        self.inventory  = []
        self.metrics    = {}
        self.environment = None
        life.animate(self)

    def __setattr__(self, attr, value):
        """ Sets an attribute within the object.

            :param  attr:       The attribute being set.
            :type   attr:       mixed

            :param  value:      The value of `attr`.
            :type   value:      mixed

            :returns:            None

            First checking for custom setters and exclusion from the 
            `Properties` dict, `__setattr__` sets attributes within the
            Entity.
        """
        if "_set_%s" % (attr,) in dir(self):
            return object.__getattribute__(self, "_set_%s" % (attr,))(value)
        elif attr in self.exclude or attr in self.__dict__:
            self.__dict__[attr] = value
            return
        else:
            if type(attr) is list:
                self.__dict__['properties'][attr] = PersistList(self, value)
            elif type(attr) is dict:
                self.__dict__['properties'][attr] = PersistDict(self, value)
            else:
                self.__dict__['properties'][attr] = value
            return

    def __getattr__(self, attr):
        """ Gets the value of `attr` from the current entity.

            :param  attr:       the attribute whose value you want returned.
            :type   attr:       mixed

            :returns:           the value of `attr`.

            First checking for a custom getter or exclusion from the 
            properties dict, `__getattr__()` returns the value of `attr`.
        """
        try:
            return object.__getattribute__(self, '_get_%s' % (attr,))() 
        except:
            if attr in self.exclude:
                return self.__dict__[attr]
            else:
                return self.__dict__['properties'][attr]

    def __delattr__(self, attr):
        """ Deletes an attribute from the entity.

            :param  attr:       the attribute to be deleted.
            :type   attr:       mixed

            Not much more to this one.  Deletes `attr` from the entity.
 
            :warning: If `attr` is in the entity's `exclude` list, deleting it 
            is probably dangerous and will break the entity, if not huge parts 
            of the MUD.
        """
        if hasattr(self, "_del_%s" % (attr,)) and not attr.startswith('_del_'):
            return getattr(self, "_del_%s" % (attr,))
        elif attr in self.exclude:
            self.warning('Deleting excluded variable; THIS IS DANGEROUS')
            del self.__dict__[attr]
        else:
            del self.properties[attr]

    def _set_name(self, name):
        """ Custom setter for the entity's `name`.

            :param  name:   The name that the entity will appear as in-game.
            :type   name:   str

            :returns:       boolean

            As any name must also be a nametag for the entity, when setting an 
            entity's name, the former name is removed from the `nametags` list 
            and the new name, `name`, is added.
        """
        if isinstance(name, str) is True:
            try:
                self.nametags.remove(self.name)
            except:
                pass
            self.properties['nametags'] += name.lower().split()[-1]
            self.properties['name'] = name
            return True
        else:
            return False

    def _get_environment(self):
        """ Returns the current environment for the entity.

            :returns:   obj
 
            Returns the environment that entity is within, which is also an 
            entity.  As the `environment` variable is stored as a reference 
            ID, we need this custom getter.
        """
        return MongoDB().get_clone(self.__dict__['properties']['environment'])

    def move(self, destination):
        """ Moves the entity to a different environment.

            :param  destination:        The desired destination.

            :returns: boolean

            Remove the entity from its current `environment` and move it into 
            `destination`, if possible.
        """
        if isinstance(destination, Entity) is True:
            destination.inventory.append(self.ent_id)
            if self.environment is not None:
                self.environment.inventory.remove(self.ent_id)
            self.environment = destination
            return True
        else:
            return False

    def remove(self):
        """
            .. todo:: Write the actual remove() function.
        """
        if type(self.environment) is not None:
            self.environment = None
        return

    def destroy(self):
        """
            .. todo:: Write the actual destroy() function.
        """
        self.remove()
        stirling.MDB.clones.remove(self.ent_id)
        del stirling.MDB.loaded_clones[self.ent_id]
        return

    def save(self):
        """ Force a save of the entity's properties. """
        self.properties.save()
        return

class Properties(dict):
    """ Properties are the attributes of an entity which are persistent.
    """
    def __init__(self, parent, from_dict=None, from_db=False):
        """ Create a new dict within the MongoDB collection `clones`.

            :param  parent:     The entity who the properties belong to.
            :type   parent:     object

            :param  from_dict:  The dict of properties to be applied 
                                    immediately.
            :type   from_dict:  dict

            :param  from_db:    Whether or not we are loading the object.
            :type   from_db:    boolean

            :returns:           None

            Create and prepare the database entry for this clone, or load the 
            properties of an existing clone.
        """
        if type(from_dict) is dict:
            dict.__init__(self, from_dict)
        else:
            dict.__init__(self, [])
        if not from_db:
            self['ent_id']     = stirling.MDB.clones.insert(self)
            self['_class']  = parent.__class__.__name__
            self['_module'] = parent.__class__.__module__
            parent.__dict__['ent_id'] = self['ent_id']
            stirling.MDB.loaded_clones[self['ent_id']] = parent
        return

    def __setitem__(self, item, value):
        """ Sets the property `item` to `value` and saves.
        """
        result = dict.__setitem__(self, item, value)
        stirling.MDB.clones.save(self)
        return result

    def __getitem__(self, item):
        """ Returns the value of `item`.
        """
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return None

    def __delitem__(self, item):
        """ Deletes the property `item` and saves.
        """
        result = dict.__delitem__(item)
        stirling.MDB.clones.save(self)
        return result

    def save(self):
        """ Save the database record for this entity's properties.
        """
        stirling.MDB.clones.save(self)
        return

class NameTags(PersistList):
    """ Nametags are a list of the nouns with which an entity may be addressed.
    """
    def __init__(self, parent, _list):
        """ Create a new :class:`persistList 
            <stirling.daemons.mongodb.persistList>` for nametags.

            :param  parent:     The entity who the nametags belong to.
            :type   parent:     object

            :param  _list:      Nametags to be created immediately.
            :type   _list:      list

            :returns:           None

            Creates a new persistent list containing the nametags of the 
            entity.  For more information about what nametags are, see 
            :term:`the glossary entry <nametag>`.
        """
        super(NameTags, self).__init__(self, _list)
        list.__init__(self, _list)
        self.parent = parent

    def append(self, item):
        """ Check to see if the nametag exists, and if not, add it.

            :param  item:       The nametag you wish to add.
            :type   item:       str

            :returns:           boolean
        """
        if isinstance(item, str):
            if self.parent.properties['nametags'].count(item) is 0:
                PersistList.append(self, item)
                return True
        return False

    def remove(self, item):
        return PersistList.remove(self, item)
