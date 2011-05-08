import stirling
from stirling.obj.room import Room

class Street(Room):
    def __init__(self):
        super(Street, self).__init__()
        self.name = 'example room'
        self.desc = 'This room demonstrates how I\'d love for the API to look'
        self.items = {
        # Is this spacing legal?
          ['list','of','synonyms']:
            ['Description of thing',['adjective','adjective']]
          }
        self.exits = {
          'east' : '1234asdf' # How would the dev know the id?  Could we wrap 
                              # exits' setter to check if it's an id or path?
          }
        # In the following line, I imagine stirling.clone() would return the 
        # ID of the instance.
        self.exit['west'] = (stirling.clone('world.dev.room.garden'))
        
