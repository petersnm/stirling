""" An entity that occupies space and has mass.

    .. module:: stirling.multiverse.matter
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    `Matter` is one of the four domains of the :mod:`multiverse 
    <stirling.multiverse>`, and is a property of any :mod:`entity 
    <stirling.entities>`.  It is notable for having volume and mass.
"""

from stirling.entities import Entity
from stirling.daemons.mongodb import PersistDict

class Matter(Entity):
    """ An entity which exists in space and has mass.

        :var    mass:   Mass is the quantitative measure of an instance of 
                        matter's resistance to acceleration.
        :type   mass:   float 
    """
    def __init__(self, name, **kw):
        """ Initialize a new instance of matter.

            :param  name:       The entity's proper name.  Should be written 
                                  as it should be rendered in game.
            :type   name:       str
            :param  **kw:       Any arguments are passed to the parent class 
                                  via :py:func:`super`.
        """
        super(Matter, self).__init__(**kw)
        self.name = name
        self.ids = {'object','entity'}
