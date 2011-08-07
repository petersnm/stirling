""" The inheritable for lifeforms in the Eukaryota kingdom.
"""

import stirling
from stirling.entities import Entity
# This is my favorite line of code, ever.  -- emsenn
from multiverse import life

class Eukaryote(Entity):
    """ The defining entity for eukaryotes.
    """
    def __init__(self, **kw):
        """ Creates a new eukaryote and sets some default properties, before 
            animating it.
        """
        super(Eukaryota, self).__init__(**kw)
        self.name       = 'eukaryote cell'
        self.nametags   = ['eucaryote', 'eukarya', 'cell']
        self.desc       = 'This eukaryote is defined by its abundance of '
                          'organelles and cytoskeleton.'
