"""
/lib/std/room.py
emsenn@Stirling 190411

    The base room inheritable
"""

from stirling.obj.object import MasterObject

class Room(MasterObject):
    def __init__(self):
        super(Room, self).__init__()
        self.rm_nametag('object')
        self.lookables = {}
        self.exits = {}
    def write(self, data):
        """
        write(text)
        
        Outputs the string text to everything in the room's inventory.
        """
        # Need to add a link to the microsyntax interpretter when we have it.
        for item in self.inventory:
            item.tell(data+'\n')
    	#Insert a control structure to place the exits within this text.
    
    #Exit functions
    def set_exits(exit_dict):
    	self.exits = exit_dict
    def add_exit(dir, obj, hidden=False):
    	self.exits[dir] = (obj, hidden)
    def remove_exit(dir):
    	del exit[dir]
    def exits(visible=True):
    	results_array = []
    	if visible == True: #return only the visible exits
    		for dir in self.exits: #Iterate through the exits
    			if self.exits[dir][1] == False: #Selects the visible exits
    				results_array.append(dir)
    		return results_array #Hopefully this indentation is correct
    	else: #This allows for the system and creators to see all exits
    		return keys(self.exits)