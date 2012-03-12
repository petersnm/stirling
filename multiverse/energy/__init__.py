""" Energy is that which enables matter to do work.

    .. module:: stirling.multiverse.energy
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    `Matter` is one of the four domains of the :mod:`multiverse 
    <stirling.multiverse>`, and is the thermodynamic quantity equivalent 
    to the capacity of a physical system to do work.  Energy is measured in 
    joules. As work is done, time progresses.  Or possibly the other way 
    around.  We aren't sure yet.
"""

from stirling.entities import Entity
from stirling.daemons.mongodb import PersistDict

class Energy(Entity):
    """ 
    """
    def __init__(self, **kw):
        """ Initialize a new instance of matter doing work.

            :param  **kw:       Any arguments are passed to the parent class 
                                  via :py:func:`super`.
        """
        super(Energy, self).__init__(**kw)
