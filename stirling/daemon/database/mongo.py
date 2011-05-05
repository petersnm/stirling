"""
    The daemon object for talking to the database
"""

import logging
logger = logging.getLogger(__name__)
logger.debug('Imported')

from pymongo import Connection

# needs moar config

MongoDB = Connection().stirling
logger.debug('Database initialized')
