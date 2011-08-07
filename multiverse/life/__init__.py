""" The living module enables things to be animate.
"""

import stirling
from stirling.daemons.mongodb import PersistList

def animate(entity):
    """ Makes `entity` alive.
    """
    if entity.verbs is None:
        entity.verbs = ['standard']
    entity.parse = parse
    entity.do_action = do_action
    return True

def parse(entity, message):
    """ Parse a NL command.
    """
    return message

def do_action(self, to_do):
    return to_do
