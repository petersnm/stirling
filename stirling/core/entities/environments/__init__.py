import stirling
from stirling.core.entities import Entity
from stirling.core.daemons.mongodb import PersistList

class Enviroment(Entity):
    def __init__(self, **kw):
        super(Environment, self).__init__(**kw)
        self.name = "environment"
        self.desc = "This is an environment."
        self.exits = Exits(self, [])


class Exits(PersistList):
    def __init__(self, parent, _list):
        super(Exits, self).__init__(self, _list)
        list.__init__(self, _list)
        self.parent = parent

    def append(self, item):
        if isinstance(item, tuple):
            if (type(tuple[0]), type(tuple[1]), type(tuple[2])) is\
              (str, str, int):
                PersistList.append(self, item)
                return True
        return False
