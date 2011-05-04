"""
The main server of the MUD, this file handles the socket server and its clients.  
This most likely needs to be expanded to handle telnet command characters, MCCP, and
MXP.
"""

import socket
import select
import random
import string
from random import choice
import stirling

from stirling.obj.spec.daemon import Daemon
from stirling.obj.spec.player import Player
from stirling.daemon.objects import load_object, get_object

class MUDServer(Daemon):
    '''MUDServer() is used to create a socket server capable of handling text 
    clients.  These clients are expected to be using, at most basic, netcat, 
    and on the more sophisticated end, clients like Mudlet and MUSHClient'''
    def __init__(self, addr, **kw):
        super(MUDServer, self).__init__(**kw)
        self.exclude += ['socket', 'connections', 'logging_in',
        'connections_player']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(addr)
        self.socket.listen(10)
        self.connections = []
        self.logging_in = []
        self.connections_player = {} #{connection: player} mapping

    def handle(self):
        # Could someone explain what these are for? -- emsenn
        r, w, e = select.select([self.socket] + self.connections, [], [], 5)
        for conn in r:
            if conn is self.socket:
                (new_conn, addr) = conn.accept()
                self.connections.append(new_conn)
                # Add them to the login queue.
                self.logging_in.append(new_conn)
                # Connects are shown this first.
                # TODO: Negotiate MCCP
                # TODO: Negotiate MXP
                new_conn.send(bytes('{0}\nv{1}\n    {2}\n\n{3}\n'.format(stirling.MUD_NAME, 
                  stirling.MUD_VERSION, choice(stirling.MUD_SPLASH), stirling.MUD_GREET), 'ascii'))
                self.info('New player connected.')
            elif conn in self.connections:
                # Sterilize input HERE
                recv_data = conn.recv(1024)
                if recv_data == '':
                    # Connection closed.
                    conn.close()
                    self.info('Player {0} disconnected.'.format(self.connections_player[conn].name))
                    self.connections.remove(conn)
                else:
                    if conn in self.logging_in:
                        # Outline the login process here!
                        # Fine if username exists/is valid: find_user(recv_data)
                        # if find_user(ster_data) is False:
                        #   new_char(ster_data)
                        # else:
                        #   login_char(ster_data)
                        username=''.join(random.choice(string.ascii_lowercase) for x in range(8))
                        player = Player(conn)
                        player.name = username
                        self.connections_player[conn] = player
                        foobar = load_object('world.testsuite.room.garden.Garden')
                        self.debug(foobar)
                        player.move(foobar)
                        self.logging_in.remove(conn)
                        conn.send(b'You are now logged in, congrats.\n')
                        self.info('Player logged in as {0}'.format(username))
                    else:
                        # If they've been logged in, pass the text to the player's
                        # object.
                        decoded_data = recv_data.decode(errors='replace')
                        player = self.connections_player[conn]
                        self.debug('Received data from {0}: {1}'.format(player.name, decoded_data))
                        player.handle_data(decoded_data)
    def handle_forever(self):
        while True:
            self.handle()

def runserver():
    server = MUDServer(('0.0.0.0', 5878))
    try:
        server.handle_forever()
    except KeyboardInterrupt:
        server.info('Received ^C, closing down')
        for c in server.connections:
            c.close()
        server.socket.close()
        server.info('Sockets closed, goodbye')
        exit()
