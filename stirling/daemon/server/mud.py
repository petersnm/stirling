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

class MUDServer(Daemon):
    '''MUDServer() is used to create a socket server capable of handling text 
    clients.  These clients are expected to be using, at most basic, netcat, 
    and on the more sophisticated end, clients like Mudlet and MUSHClient. 
    [server, mud server]'''
    def __init__(self, addr, **kw):
        '''Create the socket server and listen for new connections.'''
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
        '''All text input from a connection gets sent here'''
        # Could someone explain what these are for? -- emsenn
        r, w, e = select.select([self.socket] + self.connections, [], [], 5)
        for conn in r:
            # If the connection is in the socket's list still, they've just 
            # arrived and need to be started down the login process.
            if conn is self.socket:
                (new_conn, addr) = conn.accept()
                self.connections.append(new_conn)
                # Add them to the login queue.
                self.logging_in.append(new_conn)
                # Connects are shown this first.
                splash = '{0}\nv{1}\n    {2}\n\n{3}\n'.format(
                  stirling.MUD_NAME,
                  stirling.MUD_VERSION, 
                  choice(stirling.MUD_SPLASH),
                  stirling.MUD_GREET)
                new_conn.send(splash.encode())
            elif conn in self.connections:
                # Sterilize input HERE
                # SERIOUSLY.  THIS WHOLE SERVER CRASHING EVERY TIME SHIT GETS OLD
                recv_data = conn.recv(1024)
                # If we aren't getting any data, kick them out of the MUD.
                if recv_data == '':
                    # Connection closed.
                    conn.close()
                    self.info('Player {0} disconnected.'.format(
                      self.connections_player[conn].name))
                    self.connections.remove(conn)
                else:
                    if conn in self.logging_in:
                        # Outline the login process here!
                        # Fine if username exists/is valid: find_user(recv_data)
                        # if find_user(ster_data) is False:
                        #   new_char(ster_data)
                        # else:
                        #   login_char(ster_data)
                        username=''.join(random.choice(string.ascii_lowercase)
                          for x in range(8))
                        player = stirling.clone('stirling.obj.spec.player.Player',
                                conn)
                        player.name = username
                        self.connections_player[conn] = player
                        foobar = stirling.search('world.testsuite.room.garden.Garden')
                        self.debug(foobar)
                        if foobar:
                            self.debug("Room found!")
                            room = foobar[0]
                        else:
                            self.debug("Cloning in new room..")
                            room = stirling.clone('world.testsuite.room.garden.Garden')
                        self.debug(room)
                        player.move(room)
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
