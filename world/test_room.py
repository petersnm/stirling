import stirling

class testRoom(stirling.core.entities.Entity):
    def __init__(self, **kw):
        super(testRoom, self).__init__(**kw)
        self.name = "test room"
        self.desc = "This here is a test room!"
        self.exits = {
            "north" : "world.room2"
          }
        
