from stirling.daemon.database import MongoDB

objects = {}

class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        self.parent = parent
        # this is becasue if it's from the DB, we dont' need to fill the db, but if it isn't, we do.
        if not from_db:
            self['_id'] = MongoDB.objects.insert(self)
            self.parent.__dict__['_id'] = self['_id']
            self['_class'] = self.parent.__class__.__name__
            self['_module'] = self.parent.__class__.__module__
            objects[self['_id']] = self.parent

    
    def __setitem__(self, item, value):
        try:
            self.parent.debug('item set '+item+":"+value)
        except:
            pass
        dict.__setitem__(self, item, value)
        MongoDB.objects.save(self)

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        dict.__delitem__(item)
        MongoDB.objects.save(self)

    def save(self):
        MongoDB.objects.save(self)

