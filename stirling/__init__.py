""" The main module for the Stirling Engine.
    
    .. module::    stirling
        :synopsis: Stirling MUD engine

    .. moduleauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    The main module for :doc:`the Stirling Engine <index>`, this sets up some 
    of the constants that are used through Stirling's operation and acts as a 
    global config file for the engine.  In addition, it defines the 
    :class:`BaseObj class <stirling.BaseObj>`, which creates the methods 
    needed by almost all of Stirling's :term:`entities <entity>` and 
    :term:`daemons <daemon>`.

    .. note:: If you wish to run Stirling, you should use :module:`run_engine` 
        as an executable.

    The following is a table of all constants which may be set in this module. 

    +-------------+------------------------------------------------------------+
    |  Constant   |                         Value                              |
    +=============+============================================================+
    |    HOST     | Host to serve through.  '``localhost``' for debugging,     |
    |             |  '``0.0.0.0``' for production.                             |
    +-------------+------------------------------------------------------------+
    |    PORT     | Port to serve on.  Default is ``5878``.                    |
    +-------------+------------------------------------------------------------+
    |   DOC_URL   | A HTTP URI pointing to Stirling's documentation.           |
    +-------------+------------------------------------------------------------+
    |     MDB     | reference to an instance of                                |
    |             | :class:`MongoDB <stirling.core.daemons.mongodb.MongoDB>`   |
    +-------------+------------------------------------------------------------+
    |   MUD_NAME  | The name of the MUD you're running                         |
    +-------------+------------------------------------------------------------+
    | MUD_VERSION | The version of the engine you're running.                  |
    +-------------+------------------------------------------------------------+
    | MUD_SPLASH  | A list of random messages rendered upon connection, after  |
    |             | the name and version.                                      |
    +-------------+------------------------------------------------------------+
    |  MUD_GREET  | A message shown to players upon connection.                |
    +-------------+------------------------------------------------------------+
    | ENTRY_ROOM  | The room which will be cloned first and attempted to be    |
    |             | loaded on reboot.                                          |
    +-------------+------------------------------------------------------------+
"""
import logging

from stirling.daemons.mongodb import MongoDB

HOST = '0.0.0.0'
PORT = 5878

MDB  = MongoDB()


DOC_URL     = 'http://emsenn.com/stirling/'
MUD_NAME    = 'Stirling'
MUD_VERSION = '0.1.0'
MUD_SPLASH = [
    'Oh bfo!',               'We love panthers!', 
    'PRAISE BEETROOT!',      'It isn\'t work',
    'Not Canland!',          'Probably illegal!', 
    'Grue-free!',            'Featureless!', 
    'Both fun and Fun!',     'Bane of Productivity!',
    'Way to go, sunshine!',  'Forget about the bunnies!',
    'Hello, Bigfoot.',       'It\'s a bucket of rainbows.',
    'Twenty-seven.',         'Mongoose fedora.',]
MUD_GREET = ('Welcome to the Stirling MUD.  We are currently in early alpha; '
    'please see https://github.com/emsenn/stirling for details.\n\n'
    'Please input your [desired] username and hit enter.')

ENTRY_ROOM = 'world.loc.afterlife.Entry'
