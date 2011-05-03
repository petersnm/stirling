import stirling
from stirling.lib.obj.room import Room

class Cafe(Room):
    def __init__(self, **kw):
        super(Cafe, self).__init__(**kw)
        # The name is the official title of a thing.
        self.name = 'cafe'
        # Nametags are the nouns which it is.
        self.nametags.append(['cafe','bar','restaurant'])
        self.desc = 'This is a small brick building, resting at the intersection '
          'of two small streets.  A counter behind which lies a variety of brewing '
          'paraphenalia is offset from the north wall, while a door south leads '
          'out into the test town'
        '''self.lookables = {
          ['building','cafe','bar','restaurant',]:(['brick','small'],
            self.desc),
          ['streets','roads',]:(['two',],
            'There are two streets intersecting with each other directly '
            'outside the cafe.  A few people walk by.'),
          ['paraphenalia','machine','assembly','piping']:(['brewing','coffee','espresso',
            'convoluted','brass',],
            'There is a large convoluted assembly of brass piping behind the '
            'counter.'),
          ['counter',]:([],
            'There is a counter set out about two meters from the north wall.'),
          }
        self.exits = {
          'south' : 'world.dev.room.street', # Implicitly add hidden flag as false?
          }'''
