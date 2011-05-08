'''
Part of the test suite, this is an example garden.  At the moment it simply 
demonstrates available room functions, nothing special.
'''

from stirling.obj.room import Room

class Garden(Room):
    def new(self):
        super(Garden, self).new()
        self.name = 'peaceful garden'
        self.desc = ('Enclosed by a tall wooden fence, this small grassy '
          'garden seems very private.  There is a small stone bench nestled '
          'against the trunk of a blossoming cherry tree, short dense grass '
          'filling the rest of the area.  There is a door leading into the '
          'house to the south.')
