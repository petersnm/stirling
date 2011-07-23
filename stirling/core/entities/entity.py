import stirling
from stirling.core.daemons import MongoDB

class Entity(stirling.core.BaseObj):
    def __init__(self, from_dict={}, from_db=False, **kw):
        super(Entity, self).__init__(**kw)
        from stirling.core.entities import Properties
        self.__dict__['exclude'] = ['properties', 'logger', 'debug', 'info',
          'warning', 'error', 'save', 'move', 'remove', 'tell',
          '_get_environment', 'set_name']
        self.__dict__['customs']       = ['name']
        self.__dict__['properties']    = Properties(self, from_dict, from_db=from_db)
        self.name,     self.desc       = ''
        self.nametags, self.inventory  = []
        self.metrics                   = {}

    def __setattr__(self, attr, value):
        if "_set_%s" % (attr,) in dir(self):
            return object.__getattribute__(self, "_set_%s" % (attr,))(value)
        elif attr in self.exclude or attr in self.__dict__:
            self.__dict__[attr] = value
            return
        else:
            self.__dict__['properties'][attr] = value
            self.save()
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

    def move(self, destination):
        pass

    def remove(self):
        pass

    def destroy(self):
        pass


class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        if not from_db:
            self['_id']     = MongoDB.entities.insert(self)
            self['_class']  = parent.__class__.__name__
            self['_module'] = parent.__class__.__name__
            parent.__dict__['_id'] = self['_id']
            MongoDB.entities[self['_id']] = parent

    def __setitem__(self, item, value):
        what = dict.__setitem__(self, item, value)
        MongoDB.entities.save(self)
        return what

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        what = dict.__delitem__(item)
        MongoDB.entities.save(self)
        return what
