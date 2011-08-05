""" The core of Stirling.

    .. module:: stirling
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    This module and submodulse are the core features which are required for 
    Stirling to operate.  Containing the definitions for the most basic of 
    entities and daemons, this module is limited to the things which Stirling 
    *needs* to operate.

"""

import logging

import stirling

class BaseObj(object):
    """
        .. module:: BaseObj()
            :synopsis:      The absolute parent for almost all stirling objects.
        .. moduleauthor::   Morgan Sennhauser <emsenn@emsenn.com>
        .. versionadded:    0.1

        BaseObj is the absolute parent for almost every other class created by 
        Stirling, with the exception of threaded daemons. At this point, the 
        BaseObj() only simplifies the process of logging.

        .. todo::
            Add logging to text files
        .. todo::
            Discuss writing error codes to help sort them
    """
    def __init__(self):
        """ Initialize the BaseObj.

            :returns: None
        """
        # The reason we add it to self.__dict__ instead of directly assigning 
        # it is related to MongoDB's persistent magic.
        # For more information, see stirling.core.entities.Entity and 
        # stirling.core.daemons.MongoDB
        self.__dict__['logger'] = logging.getLogger(self.__module__)
        return


    def debug(self, message):
        """Sends the debug `message` to the console.

            :param  message:     Message containing the debug information
            :type   message:    str

            :returns:           None
        """
        self.__dict__['logger'].debug(message)
        return


    def info(self, message):
        """Sends an informative ``message`` through ``BaseObj().logger``.
 
            :param  message:    Informational messages about the MUD.
            :type   message:    str
            :returns: None
        """
        self.__dict__['logger'].info(message)
        return


    def warning(self, message):
        """Sends a warning ``message`` through ``BaseObj().logger``.

            :param  message:    A string explaining the warning condition.
            :type   message:    str

            :returns: None
        """
        self.__dict__['logger'].warning(message)
        return

    def error(self, message):
        """Sends an error ``message`` through ``BaseObj().logger``.

            :param  message: A string explaining the error that has occurred.
            :type   message: str

            :returns: None
        """
        self.__dict__['logger'].error(message)
        return
