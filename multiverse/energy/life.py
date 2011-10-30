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
import functools

def animate(entity):
    """ Breathe life into `entity`.

        :param      entity:     The entity
    """
    print(entity)
    if entity.verbs is None:
        entity.verbs = ['standard']
    entity.__dict__['exclude'] += ['parse', 'do_action']
    entity.parse = functools.partial(parse, entity)
    entity.do_action = functools.partial(do_action, entity)
    return True

def parse(entity, message):
    """ Parse a NL command.
    """
    spl = message.split(' ')
    if len(spl) > 1:
        cmd = spl[0]
        targs = spl[1:]
    else:
        cmd = spl[0]
        targs = []
    kwargs = {}
    args = []
    for arg in targs:
        if arg.startswith('--'):
            if '=' in arg:
                targ = arg[2:].split('=', 1)
                if len(targ) == 2:
                    kwargs[targ[0]] = targ[1]
        elif arg.startswith('-'):
            for char in arg[1:]:
                kwargs[char] = True
        else:
            args.append(arg)
    entity.debug("%s | %s | %s" % (cmd, kwargs, args))
    entity.debug('parsed: %s' % (message,))
    return message

def do_action(self, to_do):
    """ Cause the living entity to do `to_do`
    """
    return to_do
