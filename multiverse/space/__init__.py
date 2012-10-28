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


"""

Ooookay, so this comment is going to be me explaining how I want space 
to work on Stirling.

Space is going to be a coordinate grid, designed after how longitude and 
latitude allocations.  So, 0 on X and 0 on Y is going to be the northern 
magnetic pole of a planet, for example.  Z's 0 will be the exact center of 
the plane.

Items will be stored be stored in volumes of space representing one unit of distance 
within the plane.  Distances of which quantitative qualities of matter 
affect other matter will be stored within that matter, and when matter 
is moved to or within a volume of space, the matter which is affected 
by those qualities are associated within the volume.

(EDIT: Possible need for special daemons which exist outside of space but 
modify quantitative values of space.  For example, the multiverse's star 
may not be an entity, but be a daemon which provides light and heat to 
the multiverse.)

For example:

class Space(Entity):
    def __init__(self, **kw)
    super(Space, self).__init__(**kw)


    def move(object, location):
        if(type(object) == object and size(location) == 3)
            

class Volume(Entity):
    def 
class Multiverse(Entity):
    def __init__(self, **kw):
    super(Multiverse, self).__init__(**kw)
    # Create a chunk of iron
    core = stirling.clone_entity('matter.elements.iron')
    # Give it a radius of 20000m, 20km.  How do we define that this object is 
    # a sphere?  core.shape = "sphere" seems silly, but specifying what matter's
    # dimensions mean by stating what shape it is, also seems handy.  Easier 
    # for developers to do "core.shape = "cylinder"" than define what a cylinder 
    # is when building any object.
    core.radius = 20000
    space.move(core)

"""
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
