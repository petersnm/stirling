#!/usr/bin/python3.2
"""

    .. module:: stirling.runengine
        :synopsis: Start the Stirling Engine
    .. moduleauthor:: Hunter Carroll <abzde@abzde.com>
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    When the :func:`start_core()` function is called, the multiverse will 
    kick into existence.
"""
import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.abspath('../'))

from stirling.multiverse import SEED_ROOM
from stirling.daemons import Mongo
from stirling.daemons.servers import MUD, HTTP

def start_core():
    """ Start the core elements of the engine.

        :returns: True or False depending on whether or not the engine started.

        First instancing the :class:`MUD Server <stirling.daemons.MUDServer>` 
        and then verifying that there is an entry point into the universe, 
        this function starts the MUD on its merry way.

        This function relies on the following constants:

        * ``stirling.HOST`` and ``stirling.MUD_PORT`` to determine where to 
          bind the :class:`MUD server <stirling.daemons.MUDserver>`
        
        * ``stirling.HOST`` and ``stirling.HTTP_PORT`` to determine where to
          bind the :class:`HTTP server
          <stirling.daemons.servers.http.HTTPServer>`

        * ``multiverse.SEED_ROOM`` to determine where to start loading the 
          multiverse from, if none exists already.
    """
    if Mongo.search_clones(SEED_ROOM) is None:
        Mongo.clone_entity(SEED_ROOM)

    MUD.start()
    HTTP.start()
    return True

if __name__ == '__main__':
    try:
        start_core()
    except KeyboardInterrupt:
        print('Server shutting down...')
        exit()
