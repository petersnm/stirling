""" The entry to the afterlife.

    .. module:: stirling.multiverse.space.afterlife.entrance
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1
"""

from stirling.multiverse.space import Room

class Entrance(Room):
    """ The entrance to the afterlife.
    """
    def __init__(self, **kw):
        """ Create a new instance of the entrance.
        """
        super(Entrance, self).__init__(**kw)
        self.name = 'entrance to the afterlife'
        self.desc = ('This is the entrance to the afterlife.  Not much thought '
                    'has been put into what it looks like, though.')
        return
