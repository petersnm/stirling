""" This module contains the MUDServer class.

    .. module:: stirling.daemons.server.mud
        :synopsis: The main MUD socket server
    .. modauthor: Hunter Carroll <abzde@abzde.com>
    .. modauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    Containing the MUDServer daemon, :mod:`stirling.daemons.servers.mud` 
    handles the logging in of users from a socket connection.
"""
import hashlib
import logging
import socket
import select
import random
import threading
import functools
from datetime import datetime

import stirling
from stirling.daemons import Mongo
from stirling.multiverse.energy.life import animate

class MUDServer(threading.Thread):
    """ The MUD server is the main method of connection for users and 
        developers.  Outputting and receiving information in textual format, 
        MUDServer provides the methods necessary for users to register, log in, 
        and of course, interact with the Stirling engine.
    """
    def __init__(self, addr, **kw):
        """ Initialize the socket server and set up a logger.

            :param  addr:       A tuple of (``Host``, ``Port``).
            :type   addr:       tuple

            :param  \*\*kw:     Any additional keywords are passed to the 
                                  parent, in this case, 
                                  :py::class:`threading.Thread`.
            :type   \*\*kw:     mixed

            :returns: True or false, whether or not the server started.

            Creates a new socket server and binds it to `addr`, which is 
            ``(stirling.HOST``, stirling.MUD_PORT)`` by default.  This socket 
            server acts as the main output of the MUD, and is therefore of 
            extremely high importance to Stirling.
        """
        super(MUDServer, self).__init__(**kw)
        self.log = logging.getLogger(self.__module__)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.log.info('Attempting to bind MUDServer daemon...')
        try:
            self.socket.bind(addr)
            self.log.info('MUDServer daemon successfully bound to port %s' % 
                (stirling.MUD_PORT))
        except:
            self.log.warning('Tried to started MUDServer() when it was already '
                             'online.')
            return
        self.socket.listen(10)
        self.connections = []
        self.inbound     = []
        self.registering = {}
        self.logging_in  = {}
        self.tutorialing = {}
        self.active      = {}
        # XXX i'm almost entirely sure PEP8 says not do to extra spacing like
        # XXX that.
        self.log = logging.getLogger(self.__module__)
        return

    def run(self):
        """Called by ``MUDServer().start()``, this makes ``MUDServer``, well, 
            start.

            :returns: None

            .. todo:: Rather than have this be so simple, we could probably 
                make the while check act more efficiently
        """
        while True:
            self.handle()
        return

    def handle(self):
        """The handler for incoming data for users.

            :returns: None

            This function handles the logging in and registration of users, 
            as well as sending logged-in users' commands to their entity.
        """ 
        read  = select.select([self.socket] + self.connections, [], [], 5)[0]
        for conn in read:

            if conn is self.socket:
                new_conn = conn.accept()[0]
                self.connections.append(new_conn)
                splash = ('{0}\n'
                          '{1}\n'
                          '    {2}\n\n'
                          '{3}\n'
                          'Please enter your [desired] username.\n'.format(
                          stirling.NAME,
                          stirling.VERSION, 
                          random.choice(stirling.SPLASHES), 
                          stirling.GREETING))
                new_conn.send(splash.encode())
                self.inbound.append(new_conn)
            elif conn in self.connections:
                recv_data = conn.recv(1024).decode(errors='replace')
                if recv_data is '':
                    self.disconnect(conn)
                recv_data = recv_data.rstrip('\r\n')
                if conn in self.inbound:
                    inbound_user = Mongo.get_user(recv_data)
                    if type(inbound_user) is not dict:
                        self.inbound.remove(conn)
                        self.registering[conn] = [recv_data]
                        self.register_user(conn)
                    else:
                        self.inbound.remove(conn)
                        self.logging_in[conn] = [recv_data] 
                        self.login_user(conn)

                elif conn in self.registering:
                    self.registering[conn].append(recv_data)
                    if self.register_user(conn) is True:
                        del self.registering[conn]
                elif conn in self.tutorialing:
                    self.tutorialing[conn].append(recv_data)
                    if self.tutorial(conn) is True:
                        del self.tutorialing[conn]
                elif conn in self.logging_in:
                    self.logging_in[conn].append(recv_data)
                    if self.login_user(conn) is True:
                        del self.logging_in[conn]
                elif conn in self.active:
                    self.active[conn].parse(recv_data)
                return

    
    def make_user(self, conn, entity):
        def send(msg):
            conn.send((msg + '\n').encode())
        entity.__dict__['exclude'] += ['send']
        entity.send = send
    
    def register_user(self, registrant):
        """ Register a new user account

            .. versionadded:: 0.1

            :param  registrant:         The socket connection of the 
                                        registering user.
            :type   registrant:         :py:class:`socket`

            Guiding a player through the account registration process and, 
            optionally, through a system of simple tutorials, 
            `register_user()` sets up the following account information:

            +---------------+--------------------------------------------------+
            |      Key      |                   Value                          |
            +===============+==================================================+
            | ``username``  | The :term:`username` of the character.           |
            +---------------+--------------------------------------------------+
            | ``password``  | Stored as a sha256 hashed hexdigest, the         |
            |               | password is the account credentials needed to    |
            |               | log in.                                          |
            +---------------+--------------------------------------------------+
            | ``birthtime`` | The time at which the account was created.       |
            +---------------+--------------------------------------------------+
        """
        account = self.registering[registrant]
        stage = len(account)
        done = False
        if stage is 1:
            registrant.send('What would you like your password to be?  Please '
                            'try to make it secure and memorable.\n'.encode())
        elif stage is 2:
            registrant.send('Please re-enter your password to confirm.'
                            '\n'.encode())
        elif stage is 3:
            if account[1] == account[2]:
                registrant.send('Passwords match.  Press enter to create the '
                                'account.\n'.encode())
                
            else:
                registrant.send('Passwords do not match!  Try re-entering '
                                'your desired password.\n'.encode())
                account.remove(account[1])
                account.remove(account[1])
        elif stage is 4:
            new_entity = Mongo.clone_entity('stirling.entities.Entity')
            password = hashlib.sha256(account[1].encode()).hexdigest()
            Mongo.make_user(account[0], password, 
                                             new_entity.ent_id, datetime.now())
            new_entity.user = Mongo.get_user(account[0])
            new_entity.interactive = True
            registrant.send(('User account successfully created.  You\'re now '
                            'ready to log in, though if you\'ve never played '
                            '%s before, you may want to go through a basic '
                            'tutorial.  Would you like to do so?\n'
                            '([Y]/n)\n' % 
                            stirling.NAME ).encode())
        elif stage is 5:
            if account[4] in ['Y', 'y', 'yes', '']:
                self.tutorialing[registrant] = [account[0]]
                done = True
            elif account[4] in ['N', 'n', 'no']:
                registrant.send('Alright.  You\'re now going to be taken to '
                                'the game.  Have fun!\n'.encode())
                self.active[registrant] = Mongo.get_clone(
                                          Mongo.get_user(
                                          account[0])['ent_id'])
                animate(self.active[registrant])
                self.make_user(registrant, self.active[registrant])
                done = True
            else:
                registrant.send('That wasn\'t a valid selection.  If you '
                                'don\'t want to go through the tutorial, type '
                                '\'no\' and hit enter.  Otherwise, just hit '
                                'enter.\n'.encode())
                account.remove(account[4])
        return done

    def login_user(self, user):
        """ Guide a user through login.
        """
        account = self.logging_in[user]
        stage = len(account)
        done = False
        if stage is 1:
            user.send('What is your password?\n'.encode())
        if stage is 2:
            input_password = hashlib.sha256(account[1].encode()).hexdigest()
            attempted_user  = Mongo.get_user(account[0])
            if input_password == attempted_user['password']:
                user.send('Password correct; logging in.\n'.encode())
                self.active[user] = Mongo.get_clone(
                                    Mongo.get_user(
                                    account[0])['ent_id'])
                
                animate(self.active[user])
                self.make_user(user, self.active[user])
                self.active[user].cmds.append('stirling.multiverse.energy.meta')
                done = True
            else:
                user.send('Password incorrect; please retype it and press '
                          'enter.\n'.encode())
                account.remove(account[1])
        return done

    def tutorial(self, user):
        """ Take a user through a quick tutorial explaining how the game works.
        """
        answers = self.tutorialing[user]
        stage = len(answers) - 1
        done = False
        if stage is 1:
            message = ('This tutorial is a basic crash course in how '
                       'commands work.  If you want a more full explanation '
                       'of how how to play %s, I highly recommend reading the '
                       'documentation at %s.\n\n'
                       'Unfortunately, there isn\'t any gameplay, so there '
                       'is no tutorial here.  Hit enter to continue.\n' 
                       % (stirling.NAME, stirling.HTTP_URI))
            user.send(message.encode())
        elif stage is 2:
            self.active[user] = Mongo.get_clone(
                                Mongo.get_user(
                                self.tutorialing[user][0])['ent_id'])
            animate(self.active[user])
            self.make_user(user, self.active[user])
            done = True
        return done

    def disconnect(self, conn):
        """ Disconnect a user from the server.
        """
        if conn in self.inbound:
            self.inbound.remove(conn)
        elif conn in self.registering:
            del self.registering[conn]
        elif conn in self.logging_in:
            del self.logging_in[conn]
        elif conn in self.active:
            del self.active[conn]
        self.connections.remove(conn)
