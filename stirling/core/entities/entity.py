import stirling
from stirling.core.daemons.mongodb import MongoDB, persistList, PersistDict

class Entity(stirling.core.BaseObj):
    """
    """
    def __init__(self, from_dict={}, from_db=False, **kw):
        super(Entity, self).__init__(**kw)
        self.__dict__['exclude'] = ['properties', 'logger', 'debug', 'info',
          'warning', 'error', 'save', 'move', 'remove', 'tell',
          '_get_environment', 'set_name']
        self.__dict__['customs']       = ['name']
        self.__dict__['properties']    = Properties(self, from_dict, from_db=from_db)
        self.nametags   = nameTags(self, ['entity'])
        self.name       = 'Entity'
        self.desc       = 'This is an entity.'
        self.inventory  = persistList(self, [])
        self.metrics    = {}

    def __setattr__(self, attr, value):
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
        if hasattr(self, "_del_%s" % (attr,)) and not attr.startswith('_del_'):
            return getattr(self, "_del_%s" % (attr,))
        elif attr in self.exclude:
            self.warning('Deleting excluded variable; THIS IS DANGEROUS')
            del self.__dict__[attr]
        else:
            del self.properties[attr]

    def _set_name(self, name):
        if isinstance(name, str) is True:
            try:
                self.nametags.remove(self.name)
            except:
                pass
            self.properties['nametags'] += name.lower()
            self.properties['name'] = name
            return True
        else:
            return False

    def _get_environment(self):
        return MongoDB().get_clone(self.__dict__['properties']['environment'])

    def handle_input(self, input):
        self.debug(self.user)
        self.debug(self.environment)
        if type(self.user) is dict and self.environment is not None:
            self.debug(self.environment.desc)
        return
            

    def move(self, destination):
        if self.environment:
            self.environment.inventory.remove(self._id)
        if isinstance(destination, Entity) is True:
            self.environment = destination._id
            try:
                destination.inventory.append(self._id)
            except:
                destination.inventory = persistList(destination, [self._id])
            return True
        else:
            return False

    def remove(self):
        pass

    def destroy(self):
        pass

    def save(self):
        self.properties.save()

class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        self.db = MongoDB()
        if not from_db:
            self['_id']     = self.db.clones.insert(self)
            self['_class']  = parent.__class__.__name__
            self['_module'] = parent.__class__.__module__
            parent.__dict__['_id'] = self['_id']
            self.db.loaded_clones[self['_id']] = parent

    def __setitem__(self, item, value):
        what = dict.__setitem__(self, item, value)
        self.db.clones.save(self)
        return what

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        what = dict.__delitem__(item)
        self.db.clones.save(self)
        return what

    def save(self):
        self.db.clones.save(self)
        return

class nameTags(persistList):
    def __init__(self, parent, _list=[]):
        list.__init__(self, _list)
        self.parent = parent

    def append(self, item):
        if isinstance(item, str):
            try:
                if self.parent.properties['nametags'].count(tag) is 0:                
                    PersistList.append(self, item)
            except:
                pass
