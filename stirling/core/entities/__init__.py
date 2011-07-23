import stirling
from stirling.core.daemons import MongoDB

class PersistList(list):
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

class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        try:
            self.database = MongoDB()
        except:
            print('Failed to load MongoDB()')
        if not from_db:
            print(type(self.database.entities))
            self['_id']     = self.database.entities.insert(self)
            self['_class']  = parent.__class__.__name__
            self['_module'] = parent.__class__.__name__
            parent.__dict__['_id'] = self['_id']
            self.database.entities[self['_id']] = parent

    def __setitem__(self, item, value):
        what = dict.__setitem__(self, item, value)
        self.database.entities.save(self)
        return what

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        what = dict.__delitem__(item)
        self.database.entities.save(self)
        return what
