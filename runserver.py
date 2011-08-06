#!/usr/bin/python3.2
""" Executable to start the server.
"""
import sys
import logging
import traceback
import threading

import stirling
from stirling.core.daemons import MUDServer

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s %(name)s: %(message)s")

def start_core():
    log = logging.getLogger(__name__)
    server = MUDServer((stirling.HOST, stirling.PORT))
    if stirling.MDB.search_clones(stirling.ENTRY_ROOM) is None:
        stirling.clone_entity(stirling.ENTRY_ROOM)
    server.start()
    return

if __name__ == '__main__':
    try:
        start_core()
    except:
        print('Exitting.')
        exit()
