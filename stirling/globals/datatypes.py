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
