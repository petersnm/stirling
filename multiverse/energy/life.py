""" Life is the fatal condition of having signaling and self-sustaining 
    functions.

    .. module:: multiverse.life
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    This module contains the functions which impart the property of being 
    alive to an :term:`entity`.

    .. todo:: At the moment, being alive doesn't do the only thing it really 
        should, which is provide a way for living entities to have 
        'signalling and self-sustaining functions.'
"""

from stirling.daemons.mongodb import PersistList

def animate(entity):
    """ Breathe life into `entity`.

        :param      entity:     The entity
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
    """ Cause the living entity to do `to_do`
    """
    return to_do
