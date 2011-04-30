"""
/lib/std/room.py
emsenn@Stirling 190411

    The base room inheritable
"""

from stirling.obj.object import MasterObject

class Room(MasterObject):
    def __init__(self):
        super(Room, self).__init__()
        self.name = 'room'
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
    def set_exits(exits):
    	"""
    	set_exits(exits)
    	
    	Removes all exits, and adds the exits in the dictionary.
    	Hidden exits can be made by supplying a tuple with index 1 TRUE.
    	
    	Example:
    	set_exits({"south":"obj.rooms.foo", "curtain":("obj.rooms.hiddenfoo", TRUE)})
    	"""
    	for dir in self.exits:
    		del self.exits[dir]
    	for dir in exits:
    		if exits[dir][1]:
    			self.add_exit(dir, exits[dir][0], exits[dir][1])
    		else:
    			self.add_exit(dir, exits[dir])
    def add_exit(dir, obj, hidden=False):
    	"""
    	add_exit(string direction, string object, bolean hidden=FALSE)
    	
    	Adds a exit with the the data.
    	"""
    	self.exits[dir] = (obj, hidden)
    def remove_exit(dir):
    	"""
    	remove_exit(string direction)
    	
    	Removes an exit by direction key.
    	"""
    	del exit[dir]
    def exits(visible=True):
    	"""
    	exits(bolean visible=True)
    	
    	Returns the visible exits in the room. If visible = false, shows all 
    		exits, regardless of visibility.
    	"""
    	if visible:
            return [k for k in keys(self.exits) if self.exits[k][1]]
    	else: #This allows for the system and creators to see all exits
    		return keys(self.exits)
