""" The base object module
"""

import logging

class BaseObj(object):
    """ The base object behind all entities and daemons.
    """
    def __init__(self):
        """ The `BaseObj` serves as the base for every :term:`entity` and 
            :term:`daemon` used in Stirling. and sets up basic logging 
            functionality.
        """
        self.__dict__['logger'] = logging.getLogger(self.__module__)
        return

    def debug(self, message):
        """ Print the debug `message` to console.
        """
        return self.__dict__['logger'].debug(message)

    def info(self, message):
        """ Print the informative `message` to console.
        """
        return self.__dict__['logger'].info(message)

    def warning(self, message):
        """ Print the warning `message` to console.
        """
        return self.__dict__['logger'].warning(message)

    def error(self, message):
        """ Print the error `message` to console.
        """
        return self.__dict__['logger'].error(message)
