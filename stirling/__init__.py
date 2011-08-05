""" The main ``__init__`` for the Stirling engine
    
    .. module::    stirling
        :synopsis: Stirling MUD engine

    .. moduleauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    This module sets up some of the constants that are used through Stirling's 
    operation and acts as a global config file for the engine.  The following 
    may be set:


    +-------------+------------------------------------------------------------+
    |  Constant   |                         Value                              |
    +=============+============================================================+
    |    HOST     | Host to serve through.  '``localhost``' for debugging,     |
    |             |  '``0.0.0.0``' for production.                             |
    +-------------+------------------------------------------------------------+
    |    PORT     | Port to serve on.  Default is ``5878``.                    |
    +-------------+------------------------------------------------------------+
    |     MDB     | reference to an instance of                                |
    |             | :class:`MongoDB <stirling.core.daemons.mongodb.MongoDB>`   |
    +-------------+------------------------------------------------------------+
    |   MUD_NAME  | The name of the MUD you're running                         |
    +-------------+------------------------------------------------------------+
    | MUD_VERSION | The version of the engine you're running.                  |
    +-------------+------------------------------------------------------------+
    | MUD_SPLASH  | A list of random messages rendered upon connection, after  |
    |             |  the name and version.                                     |
    +-------------+------------------------------------------------------------+
    |  MUD_GREET  | A message shown to players upon connection.                |
    +-------------+------------------------------------------------------------+

    .. todo :: 
        Add imports to stirling/__init__.py to abbreviate
        Add more splash text thingies.
"""

from stirling.core.daemons.mongodb import MongoDB
from stirling.core.daemons.mud import MUDServer

HOST = '0.0.0.0'
PORT = 5878

MDB  = MongoDB()

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
