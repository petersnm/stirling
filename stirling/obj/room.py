"""
/lib/std/room.py
emsenn@Stirling 190411

    The base room inheritable
"""

import stirling
from stirling.obj.object import MasterObject

class Room(MasterObject):
    def __init__(self, **kw):
        super(Room, self).__init__(**kw)
    
    def new(self):
        super(Room, self).new()
        self.name = 'room'
        self.lookables = {}

    def write(self, data):
        """
        write(text)
        
        Outputs the string text to everything in the room's inventory.
        """
        # Need to add a link to the microsyntax interpretter when we have it.
        for item in self.inventory:
            item.tell(data+'\n')
    	#Insert a control structure to place the exits within this text.
