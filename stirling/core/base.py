import logging
import sys

import stirling

class BaseObj:
    """
        .. module:: BaseObj()
            :synopsis: The absolute parent for almost all stirling objects.
        .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
        .. function::   __init__()
                        debug(message)
                        info(message)
                        warning(message)
                        error(message)
        
        BaseObj is the absolute parent for almost every other class created by 
        Stirling, with the except of threaded Daemons. At this point, the 
        BaseObj() only simplifies the process of logging.
    """
    def __init__(self):
        """Give BaseObj() a ``logger`` with the name of ``BaseObj().__module__``.
            Stirling defines the configuration of the logger in :mod:`stirling`
        :returns: None
        """
        self.logger = logging.getLogger(self.__module__)
        return

    def debug(self, message):
        """Sends a debug ``message`` through the ``BaseObj().logger``.

            :param message: A string that contains the information you wish to debug.
        """
        self.logger.debug(message)
        return

    def info(self, message):
        """Sends an informative ``message`` through ``BaseObj().logger``.
 
            :param message: A string that contains information about what just 
              occured that you want to log information about.
        """
        self.logger.info(message)
        return

    def warning(self, message):
        self.logger.warning(message)
        return

    def error(self, message):
        self.logger.error(message)
        return
