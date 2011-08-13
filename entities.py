""" Entities are persistent objects which exist in Stirling's multiverse.

    .. module:: stirling.entities
        :synopsis: Stateful object class.
    .. moduleauthor:: Hunter Carroll <abzde@abzde.com>
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    An :term:`entity` is any object which has physical existence in the 
    :term:`multiverse`.  A toothpick, a `demon from the twelfth plane of 
    torment <http://buttersafe.com/2008/10/23/the-detour/>`_, and a cloud of 
    methane, are all entities.  Entities are cloned into the multiverse, and 
    persistently stored using :class:`stirling.daemons.MongoDB`.
"""

import types
from stirling import BaseObj
from stirling.daemons import Mongo
from stirling.daemons.mongodb import PersistList, PersistDict

class Entity(BaseObj):
    """ A persistent object intended to exist within Stirling's multiverse.
    """
    def __init__(self, init_dict=None, from_db=False, **kw):
        """ When a new entity is instanced, it sets up some basic attributes.

            :param  init_dict:      Applied as a dict of the entity's 
                                      properties upon creation.
            :type   init_dict:      dict

            :param  from_db:        If true, the object is loaded from the 
                                      database.  (That is to say, loaded 
                                      rather a new one created.)
            :type   from_db:        boolean

            :param  **kw:           All other arguments; passed to the parent
                                      via :py:func:`super`.
            :type   **kw:           mixed

            :return:                None

            When a new entity is created, it creates the special attribute 
            `properties` within itself.  This properties dict is an instance 
            of the :class:`Properties` class, and is what gives entities their 
            database persistence.  By overriding __setattr__ and __getattr__ 
            within entities, Stirling is able to keep track of just the 
            important information of an entity and keep it persistent, without 
            needing to be explicitly defined.
        """
        super(Entity, self).__init__(**kw)
        self.__dict__['exclude'] = ['properties']
        self.__dict__['properties']    = Properties(self, init_dict, 
                                                    from_db=from_db)
        self.nametags   = NameTags(self, ['entity'])
        self.name       = 'Entity'
        self.desc       = 'This is a nondescript entity.  It exists.'
        self.inventory  = []
        self.metrics    = {}
        self.environment = None

    def __setattr__(self, attr, value):
        """ Sets an attribute within the object.

            :param  attr:       The attribute being set.
            :type   attr:       mixed

            :param  value:      The value of `attr`.
            :type   value:      mixed

            First checking for custom setters and exclusion from the 
            `Properties` dict, `__setattr__` sets attributes within the
            Entity.
        """
        if hasattr(self, '_set_%s' % (attr,)):
            return object.__getattribute__(self, "_set_%s" % (attr,))(value)
        elif attr in self.__dict__['exclude'] or attr in self.__dict__:
            self.__dict__[attr] = value
            return
        else:
            if type(value) is list:
                self.__dict__['properties'][attr] = PersistList(self, value)
            elif type(value) is dict:
                self.__dict__['properties'][attr] = PersistDict(self, value)
            elif type(value) is types.FunctionType:
                self.__dict__[attr] = types.MethodType(value, self)
                self.__dict__['exclude'] += [attr]
            else:
                self.__dict__['properties'][attr] = value
            return

    def __getattr__(self, attr):
        """ Gets the value of `attr` from the current entity.

            :param  attr:       the attribute whose value you want returned.
            :type   attr:       mixed

            First checking for a custom getter or exclusion from the 
            properties dict, `__getattr__()` returns the value of `attr`.
        """
        if hasattr(self, '_get_%s' % (attr,)):
            return object.__getattribute__(self, '_get_%s' % (attr,))() 
        elif attr in self.__dict['exclude']:
            return self.__dict__[attr]
        else:
            return self.__dict__['properties'][attr]

    def __delattr__(self, attr):
        """ Deletes an attribute from the entity.

            :param  attr:       the attribute to be deleted.
            :type   attr:       mixed

            Not much more to this one.  Deletes `attr` from the entity.
 
            :warning: If `attr` is in the entity's `exclude` list, deleting it 
              is probably dangerous and will break the entity, if not huge 
              parts of the MUD.
        """
        if hasattr(self, "_del_%s" % (attr,)) and not attr.startswith('_del_'):
            return getattr(self, "_del_%s" % (attr,))
        elif attr in self.__dict__['exclude']:
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
            except ValueError:
                pass
            self.nametags.append(name.split()[-1].lower())
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
        return Mongo.get_clone(self.__dict__['properties']['environment'])

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
        """ Remove the entity from its current environment.
        """
        if type(self.environment) is not None:
            self.environment = None
        return

    def destroy(self):
        """ First :func:`remove` the entity and then delete it from the 
            :class:`database <stirling.daemons.MongoDB>`
        """
        self.remove()
        Mongo.clones.remove(self.ent_id)
        del Mongo.loaded_clones[self.ent_id]
        return

    def save(self):
        """ Force a save of the entity's properties. """
        self.properties.save()
        return

class Properties(dict):
    """ Properties are the attributes of an entity which are persistent.
    """
    def __init__(self, parent, init_dict=None, from_db=False):
        """ Create a new dict within the 
            :class:`MongoDB <stirling.daemons.MongoDB>` collection `clones`.

            :param  parent:     The entity who the properties belong to.
            :type   parent:     object

            :param  init_dict:  The dict of properties to be applied 
                                    immediately.
            :type   init_dict:  dict

            :param  from_db:    Whether or not we are loading the object.
            :type   from_db:    boolean

            :returns:           None

            Every entity has an attribute of `properties`, which is an 
            instance of this class, and is what gives them their database 
            persistence.  Each new instance of an entity is cloned and their
            `properties` are added to the database collection 
            ``Mongo.clones``.

            If provided, `init_dict` is a dictionary of the entity's attributes 
            to be added and saved immediately.

            If you are loading the entity from the database, `from_db` should 
            be set to equal ``True``.  If `from_db` is not true, then 
            Properties() will attempt to make a new entry into the collection 
            which is unnecessary.
        """
        if type(init_dict) is dict:
            dict.__init__(self, init_dict)
        else:
            dict.__init__(self, [])
        if not from_db:
            self['ent_id']     = Mongo.clones.insert(self)
            self['_class']  = parent.__class__.__name__
            self['_module'] = parent.__class__.__module__
            parent.__dict__['ent_id'] = self['ent_id']
            Mongo.loaded_clones[self['ent_id']] = parent
        return

    def __setitem__(self, item, value):
        """ Sets the property `item` to `value` and saves.
        """
        result = dict.__setitem__(self, item, value)
        Mongo.clones.save(self)
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
        Mongo.clones.save(self)
        return result

    def save(self):
        """ Save the database record for this entity's properties.
        """
        Mongo.clones.save(self)
        return

class NameTags(PersistList):
    """ Nametags are a list of the nouns with which an entity may be addressed.

        Nametags are any non-pronoun noun used to refer to an entity.  
        Additionally, nametags are made lowercase when they are set.
    """
    def __init__(self, parent, _list):
        """ Create a new instance of 
            :class:`persistList <stirling.daemons.mongodb.PersistList>` for
            storing nametags.:class:`persistList 
            <stirling.daemons.Mongodb.persistList>` for nametags.

            :param  parent:     The entity who the nametags belong to.
            :type   parent:     object

            :param  _list:      Nametags to be created immediately.
            :type   _list:      list


            Creates a new persistent list containing the nametags of the 
            entity.  For more information about what nametags are, see 
            :term:`the glossary entry <nametag>`.
        """
        super(NameTags, self).__init__(self, _list)
        list.__init__(self, _list)
        self.parent = parent
        return

    def append(self, item):
        """ Check to see if the nametag exists, and if not, add it.

            :param  item:       The nametag you wish to add.
            :type   item:       str

            :returns:           boolean
        """
        if isinstance(item, str):
            if self.parent.properties['nametags'].count(item) is 0:
                PersistList.append(self, item.lower())
                return True
        return False

    def remove(self, item):
        return PersistList.remove(self, item)
