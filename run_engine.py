#!/usr/bin/python3.2
"""

    .. module:: runengine
        :synopsis: Start the Engine
    .. moduleauthor:: Hunter Carroll <abzde@abzde.com>
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    When executed, this module starts everything required for Stirling to work.
"""

import logging

import stirling
from stirling.daemons import MUDServer

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s %(name)s: %(message)s")

def start_core():
    """ Start the core elements of the engine.

        :returns: True or False depending on whether or not the engine started.

        First instancing the MUDServer and then verifying there is an entry 
        point to the multiverse, :function:`start_core()` gets the Engine 
        started.
    """
    server = MUDServer((stirling.HOST, stirling.PORT))
    if stirling.MDB.search_clones(stirling.ENTRY_ROOM) is None:
        stirling.MDB.clone_entity(stirling.ENTRY_ROOM)
    server.start()
    return

if __name__ == '__main__':
    try:
        start_core()
    except KeyboardInterrupt:
        print('Server shutting down...')
        exit()
