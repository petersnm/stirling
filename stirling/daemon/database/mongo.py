"""
/lib/special/database.py
emsenn@Stirling 190411

    The daemon object for talking to the database
"""
import logging
logger = logging.getLogger(__name__)
logger.debug('Imported')

from pymongo import Connection

# needs moar config

database = Connection().stirling
logger.debug('Database init\'d')