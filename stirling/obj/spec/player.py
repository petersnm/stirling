"""
/lib/std/player.py
abzde@Stirling 100411

    The base player object - it contains the functions that are truly unique 
to players.
"""

from stirling.obj.living.living import Living

class Player(Living):
    def __init__(self, conn, **kw):
        super(Player, self).__init__(**kw)
        self.exclude += ['connection', 'handle_data']
        self.connection = conn

    def new(self):
        super(Player, self).new()
        self.cmd_modules += ['cmd.std','cmd.dev']

    def tell(self, data):
        super(Player, self).tell(data)
        self.connection.send(bytes(data, 'UTF-8'))

    def handle_data(self, data):
        self.parse_line(data)
