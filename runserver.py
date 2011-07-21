#!/usr/bin/python3.2

import sys
import logging
logging.basicConfig(level=logging.DEBUG)
import stirling


class Universe:
    def __init__(self, clean=False):
        try:
            import stirling
        except:
            print('Failed to import stirling module')
        print('Attempting to import core objects')
        try:
            self.load_core()
        except:
            print('Failed to load core objects.  This is a fatal error, and '
              'Stirling must exit.')
            exit()  
    
    def load_core(self):
        print('Loading BaseObj...')
        try:
            from stirling.core.base import BaseObj
        except:
            'BaseObj failed to import'
        print('Loading MUDServer...')
        try:
            from stirling.core.daemons import MUDServer
        except:
            print('MUDServer failed to import')
        print('Starting MUDServer...')
        try:
            server = MUDServer((stirling.HOST, stirling.PORT))
            server.start()
        except:
            print('MUDServer failed to start.  Fatal; exiting.')
            exit()
        print('Woooooooo threading!')

if __name__ == '__main__':
    print('Starting the bootstrapping process')
    Stirling = Universe()
