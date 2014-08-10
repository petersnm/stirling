""" Life is the fatal condition of having signaling and self-sustaining 
    functions.

    .. module:: stirling.multiverse.energy.life
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    This module contains the functions which impart the property of being 
    alive to an :term:`entity`.

    .. todo:: At the moment, being alive doesn't do the only thing it really 
        should, which is provide a way for living entities to have 
        'signalling and self-sustaining functions.'
"""
import functools
import traceback
import importlib

from stirling.daemons.mongodb import PersistList


def animate(entity):
    """ Breathe life into `entity`.

        :param      entity:     The entity
    """
    if entity.cmds is None:
        entity.cmds = ['stirling.multiverse.energy.std', 'stirling.multiverse.energy.meta']
    entity.__dict__['exclude'] += ['parse', 'do_action']
    entity.parse = functools.partial(parse, entity)
    entity.do_action = functools.partial(do_action, entity)
    entity.command_history = []
    return True

def parse(entity, message):
    """ Parse a command.
        :param entity:      The entity the command comes from.
        :type entity:       stirling.entity.Entity 
        
        :param command:     The command recieved.
        :type command:      str
        
        Parses a command recieved from a living. Checks for commands in the
        modules listed in `entity.cmds` and executes the command, if one is
        found.
    """
    command = message.split(' ')
    entity.command_history.append(command)
    verb = command[0]
    # TODO: check if the verb is an an alias
    entity.debug('verb is %s' % (verb,))
    if entity.environment != None:
        if verb in entity.environment.exits:
            entity.move(verb)
    entity.send('Your verb was %s' % (verb,))
    return

def do_action(self, to_do):
    """ Cause the living entity to do `to_do`
    """
    return to_do
