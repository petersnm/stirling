""" Static environment entities.

    .. module:: stirling.multiverse.space
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    `Space` is one of the four domains of the :mod:`multiverse 
    <stirling.multiverse>`, containing enviroments (frequently called 
    :term:`rooms <room>`) that don't really move, relative to the whole of the 
    multiverse.  A dusty attic, a crater on a moon, and the gates of hell are 
    all rooms.
"""

from stirling.entities import Entity
from stirling.daemons.mongodb import PersistDict

class Room(Entity):
    """ A physically static entity.
    """
    def __init__(self, **kw):
        """ Initilaize a new room.

            :param  **kw:       Any arguments are passed to the parent class 
                                  via :py:func:`super`.
        """
        super(Room, self).__init__(**kw)
        self.name = 'room'
        self.desc = ('This is a nondescript room.  It exists within the '
                    'multiverse, somewhere.')
