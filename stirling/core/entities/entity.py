mport stirling
from stirling.core.daemons import MongoDB

class Entity(stirling.core.BaseObj):
    """
        .. py:class:: Entity()
            :versionadded: 0.1.0
    """
    def __init__(self, from_dict={}, from_db=False, **kw):
        """ This is the inheritable class that defines every object in the engine.                        
        
        """
        super(Entity, self).__init__(**kw)
        self.__dict__['exclude'] = ['properties', 'logger', 'debug', 'info',
          'warning', 'error', 'save', 'move', 'remove', 'tell',
          '_get_environment', 'set_name']
        self.__dict__['customs']       = ['name']
        self.__dict__['properties']    = Properties(self, from_dict, from_db=from_db)
        self.name       = 'entity'
        self.desc       = 'This is an entity.'
        self.nametags   = ['entity']
        self.inventory  = []
        self.metrics    = {}

    def __setattr__(self, attr, value):
        """ Sets an attribute in the current class.
            :param attr: the attribute in question that you wish to change.
                :type string:
            :param value: the value you wish to set the attribubte to.
           
            ``__baseattr__`` is the base setter for every entity in the engine. The function makes checks for custom getters before doing anything. If one is found, the custom getter is called. If no custom setter is found,  the value is saved in self.__dict__['properties'][attr] unless the attribute *already exists* as self.attribute.
        """
        if "_set_%s" % (attr,) in dir(self):
            return object.__getattribute__(self, "_set_%s" % (attr,))(value)
        elif attr in self.exclude or attr in self.__dict__:
            self.__dict__[attr] = value
            return
        else:
            self.__dict__['properties'][attr] = value
            return

    def __getattr__(self, attr):
        if not attr.startswith(attr):
            try:
                return object.__getattribute__(self, '_get_%s' % (attr,))() 
            except:
                if attr in self.exclude:
                    return self.__dict__[attr]
                else:
                    return self.__dict__['properties'][attr]

    def __delattr__(self, attr):
        """
            :warning: Deleting an attribute that is in ``self.exclude`` is ***dangerous***,\
            as it breaks core functionality and the way the engine talks to the database.
        """
        if hasattr(self, "_del_%s" % (attr,)) and not attr.startswith('_del_'):
            return getattr(self, "_del_%s" % (attr,))
        elif attr in self.exclude:
            self.warning('Deleting excluded variable; THIS IS DANGEROUS')
            del self.__dict__[attr]
        else:
            del self.properties[attr]

    def move(self, destination):
        """
            :todo: Write the actual move() function.
        """
        pass

    def remove(self):
        """
            :todo: Write the actual remove() function.
        """
        pass

    def destroy(self):
        """
            :todo: Write the actual destroy() function.
        """
        pass


class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        self.db = MongoDB()
        if not from_db:
            self['_id']     = self.db.entities.insert(self)
            self['_class']  = parent.__class__.__name__
            self['_module'] = parent.__class__.__name__
            parent.__dict__['_id'] = self['_id']
            self.db.loaded_entities[self['_id']] = parent

    def __setitem__(self, item, value):
        what = dict.__setitem__(self, item, value)
        self.db.entities.save(self)
        return what

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        what = dict.__delitem__(item)
        self.db.entities.save(self)
        return what

    def save(self):
        self.db.entities.save(self)
        return
