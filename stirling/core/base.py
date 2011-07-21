import logging
import sys

import stirling

class BaseObj(object):
    '''BaseObj is the base for all things in the MUD, from a sneeze to global 
       warming to your mother. '''
    def __init__(self):
        self.logger = logging.getLogger(self.__module__)

    def debug(self, message):
        self.logger.debug(message)
        return

    def info(self, message):
        self.logger.info(message)
        return

    def warning(self, message):
        self.logger.warning(message)
        return

    def error(self, message):
        self.logger.error(message)
        return
