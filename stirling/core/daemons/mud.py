"""
    .. module:: stirling.core.daemons.mud
        :synopsis: The main MUD socket server and related functions
    .. modauthor: Hunter Carroll <abzde@abzde.com>
    .. modauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1
"""
import hashlib
import logging
import socket
import select
import random
import threading

import stirling
from stirling.core.daemons.mongodb import MongoDB
from stirling.core.entities import Entity

class MUDServer(threading.Thread):
    """
        .. module::     MUDServer()
            :synopsis: The main MUD socket server
        .. modauthor: Morgan Sennhauser <emsenn@emsenn.com>
        .. versionadded:: 0.1.0
    """
    def __init__(self, addr, **kw):
        """Initialize the socket server and set up a logger

            :param addr: A tuple of (``Host``, ``Port``).
            :type addr: tuple
            :param kw**: Any additional keywords are passed to the parent, in 
              this case, :mod:`threading.Thread`.
            :var socket: A socket object, the server iteself.
            :var connections: A list of current connections.
            :var inbound: A list of inbound connections. (Those which haven't 
                been logged in yet.)
            :var connection_user: A dict pairing connections with their user 
                properties.
            :returns: None

            Creates a new socket server and binds it to `addr`, which is 
            ``(stirling.HOST``, stirling.PORT)`` by default.  This socket 
            server acts as the main output of the MUD, and is therefore of 
            extremely high importance to Stirling.
        """
        super(MUDServer, self).__init__(**kw)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(addr)
        self.socket.listen(10)
        self.connections      = []
        self.inbound          = []
        self.registering      = {}
        self.logging_in       = []
        self.active           = {}
        self.connections_user = {} #{connection: player} mapping
        self.log = logging.getLogger(self.__module__)
        return None

    def run(self):
        """Called by ``MUDServer().start()``, this makes ``MUDServer``, well, 
            start.

            :returns: None

            .. todo:: Rather than have this be so simple, we could probably 
                make the wihle check act more efficiently
        """
        while True:
            self.handle()
        return

    def handle(self):
        """The handler for incoming data for users.

            :returns: None

            .. todo::
                Handle logging in.
                Expand the documentation/clean up this function
        """
        r, w, e = select.select([self.socket] + self.connections, [], [], 5)
        for conn in r:
            if conn is self.socket:
                (new_conn, addr) = conn.accept()
                self.connections.append(new_conn)
                splash = '{0}\nv{1}\n    {2}\n\n{3}\n'.format(
                  stirling.MUD_NAME, stirling.MUD_VERSION, 
                  random.choice(stirling.MUD_SPLASH), stirling.MUD_GREET)
                new_conn.send(splash.encode())
                self.inbound.append(new_conn)
            elif conn in self.connections:
                recv_data = conn.recv(1024).decode(errors='replace').rstrip('\r\n')
                if conn in self.inbound:
                    inbound_user = MongoDB().get_user(recv_data)
                    if type(inbound_user) is not dict:
                        conn.send('That user is not registered, to '
                          'do so, please type the password you want.\n'.encode())
                        self.inbound.remove(conn)
                        self.registering[conn] = [recv_data]
                elif conn in self.registering:
                    if len(self.registering[conn]) is 1:
                        self.registering[conn].append(recv_data)
                        conn.send('To complete registration, please re-enter '
                          'your password.\n'.encode())
                    elif len(self.registering[conn]) is 2:
                        if self.registering[conn][1] == recv_data:
                            conn.send('Passwords match, creating user account.\n'.encode())
                            new_body = MongoDB().clone_entity('stirling.core.entities.entity.Entity')
                            user_info = {
                              'username' : self.registering[conn][0],
                              'password' : hashlib.sha256(self.registering[conn][1].encode()).hexdigest(),
                              'body'     : new_body._id, }
                            new_user = MongoDB().users.insert(user_info) 
                            new_room = MongoDB().clone_entity('world.test_room.testRoom')
                            del self.registering[conn]
                            new_body.move(new_room)
                            new_body.__dict__['exclude'].append('user')
                            new_body.user = user_info
                            self.active[conn] = new_body
                        else:
                            conn.send('Password didn\'t match, what is it you '
                              'want your password to be?\n'.encode())
                            self.registering[conn] = [self.registering[conn][0]]
                elif conn in self.active:
                    self.active[conn].handle_input(recv_data)
                    self.active[conn].foo = 'bar'
                    self.log.debug(self.active[conn].foo)
                return
