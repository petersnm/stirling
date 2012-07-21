""" The multiverse is where all entities are stored.

    .. module::         stirling.multiverse
    .. moduleauthor::   Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded::   0.1

    The multiverse is where all the modules for :term:`entities <entity>` are 
    stored.  These entities are :term:`cloned <clone>` and stored persistently 
    in the :mod:`database <stirling.daemons.MongoDB>`, and it is these clones 
    which daemons, users, and of course, other clones, interact with.

    The multiverse is divided into two :term:`domains <domain>`:

    * **:mod:`Matter <stirling.multiverse.space>`** is the hierarchy of 
      entities which exist have mass and volume.  Things as 
      varied as an iguana, a couch, and two cubic meters of helium, are all 
      matter.

    * **:mod:`Energy <stirling.multiverse.energy>`** is the second domain 
      of the multiverse, and is a collection of definitions of things which 
      are work.  Sighting a rifle, collapsing into a black hole, and 
      speaking all fall under this domain.

"""

from stirling.entities import Entity
from stirling.multiverse.matter import Matter
from stirling.multiverse.energy import Energy

class Multiverse(Entity):
    """ The Multiverse is the entity within which all matter exists and all 
        energy occurs.
    """
    def __init__(self, **kw):
        """ Initialize a new instance of the multiverse.

            :returns: None
        """
        super(Multiverse, self).__init__(**kw)
        return

    def start(self):
        """ This is a debug function to test things in the Multiverse.
        """
        self.debug('Starting Multiverse.start() function...')
        self.debug('Ending Multiverse.start() function...')
        return True
