import stirling
from stirling.obj.room import Room

class Foyer(Room):
    def __init__(self, **kw):
        super(Garden, self).__init__(**kw)
        self.name = 'museum foyer'
        self.desc = 'This is the foyer of the developer museum.'
