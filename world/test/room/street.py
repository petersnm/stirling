import stirling
from stirling.obj.room import Room

class Street(Room):
    def __init__(self, **kw):
        super(Street, self).__init__(**kw)
        self.name = 'narrow street'
        self.desc = 'This is an intersection of two narrow paved streets, with '
          'a cafe situated on the north side of the road.  Two streets lead '
          'out from here; Skipper Lane to the northeast and southwest, and '
          'Jolly Avenue leading east and west.'
