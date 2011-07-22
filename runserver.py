#!/usr/bin/python3.2

import sys
import logging
import threading


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s: %(message)s")

class Universe:
    def __init__(self):
        self.log = logging.getLogger(self.__module__)
        self.log.info('Intialized, moving to importCore()')
        try:
            self.importCore()
        except:
            self.log.error('importCore() failed!  This is fatal!')
            return
        self.log.info('Moving to importModules()')
        try:
            self.importModules()
        except:
            self.log.warning('importModules() failed!  This is quite severe '
              'and means that most features you want won\'t be there!')
        self.log.info('Moving to startCore()')
        try:
            self.startCore()
        except:
            self.log.error('startCore() failed!  This is fatal!')
            return
        return

    def importCore(self):
        try:
            import stirling
        except:
            self.log.warning('stirling failed to import')
        try:
            from stirling.core.daemons import MUDServer
        except:
            self.log.warning('MUDServer failed to import')
        return

    def importModules(self):
        pass

    def startCore(self):
        try:
            server = MUDServer((stirling.HOST, stirling.PORT))
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
