from stirling.daemon.database import MongoDB
import sys
import logging
logging.getLogger('cocks')

objects = {}

class Properties(dict):
    def __init__(self, parent, from_dict={}, from_db=False):
        dict.__init__(self, from_dict)
        # this is becasue if it's from the DB, we dont' need to fill the db, but if it isn't, we do.
        if not from_db:
            self['_id'] = MongoDB.objects.insert(self)
            parent.__dict__['_id'] = self['_id']
            self['_class'] = parent.__class__.__name__
            self['_module'] = parent.__class__.__module__
            objects[self['_id']] = parent

    
    def __setitem__(self, item, value):
        wat = dict.__setitem__(self, item, value)
        try:
            MongoDB.objects.save(self)
        except Exception:
            logging.debug(sys.exc_info())
        return wat

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __delitem__(self, item):
        wat = dict.__delitem__(item)
        MongoDB.objects.save(self)
        return wat

    def save(self):
        MongoDB.objects.save(self)

