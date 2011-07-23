import logging
import socket
import select
import random
import string
import threading

import stirling
from stirling.core.entities.entity import Entity

class MUDServer(threading.Thread):
    def __init__(self, addr, **kw):
        """Initialize the socket server and set up a logger

            :param addr: A tuple of (``Host``, ``Port``).
            :param kw**: Any additional keywords are passed to the parent, in 
              this case, :mod"`threading.Thread`
            :returns: None
        """
        super(MUDServer, self).__init__(**kw)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(addr)
        self.socket.listen(10)
        self.connections = []
        self.inbound = []
        self.connections_player = {} #{connection: player} mapping
        self.log = logging.getLogger(self.__module__)
        return None

    def run(self):
        """Called by ``MUDServer().start()``, this makes ``MUDServer``, well, 
            start.

            :returns: None
        """
        self.serve_forever()
        return

    def handle(self):
        """The handler for incoming data for users.

            :returns: None

            .. todo::
                Handle logging in.
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
                recv_data = conn.recv(1024).decode(errors='replace')
                if recv_data == '':
                    self.log.info('Connection dropping')
                    self.connections.remove(conn)
                    conn.close()
                    del conn
                else:
                    if conn in self.inbound:
                        self.log.debug('testing!')
                        user = Entity()
                    pass
    
    def serve_forever(self):
        """The function that keeps ``MUDServer()`` serving.

            :returns: None

            .. todo:: Make this poll every so often, rather than as fast as 
                it can.
        """
        while True:
            self.handle()
