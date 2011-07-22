#!/usr/bin/python3.2

import sys
import logging
import traceback
import threading

import stirling
from stirling.core.daemons import MUDServer


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s: %(message)s")

class Universe:
    def __init__(self):
        self.log = logging.getLogger(self.__module__)
        try:
            self.startCore()
        except:
            self.log.error('startCore() failed!  This is fatal!')
            return
        return

    def startCore(self):
        try:
            server = MUDServer((stirling.HOST, stirling.PORT))
        except:
            self.log.warning('Failed to create MUDServer() instance.')
        try:
            server.start()
        except:
            self.log.error('MUDServer() failed to start()')
        return

if __name__ == '__main__':
    try:
        Om = Universe()
    except:
        print('Exitting.')
        exit()
