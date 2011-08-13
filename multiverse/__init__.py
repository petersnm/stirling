""" The multiverse is where all entities are stored.

    .. module::         stirling.multiverse
    .. moduleauthor::   Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded::   0.1

    The multiverse is where all the modules for :term:`entities <entity>` are 
    stored.  These entities are :term:`cloned <clone>` and stored persistently 
    in the :mod:`database <stirling.daemons.MongoDB>`, and it is these clones 
    which daemons, users, and of course, other clones, interact with.

    The multiverse is divided into four :term:`domains <domain>`:

    * **:mod:`Space <stirling.multiverse.space>`** is all the static 
      environments of the multiverse - rooms.  Be it a sandy beach, a dark 
      mine, the surface of a supernova, or three miles in the sky.  Entities 
      in this domain tend not to move, without bringing the rest of the 
      multiverse with them.

    * **:class:`Time <stirling.multiverse.space>`** is a :term:`daemon` which 
      handles the fourth dimension for the multiverse.  Within Stirling, 
      time is handled by a tick timer.

        .. todo:: A tick timer and related API need to actually be specced 
          and coded.

    * **:mod:`Matter <stirling.multiverse.space>`** is the hierarchy of 
      entities which exist in `space` and progress through `time`.  Things as 
      varied as an iguana, a couch, and two cubic meters of helium, are all 
      matter.

    * **:mod:`Energy <stirling.multiverse.energy>`** is the fourth domain 
      of the multiverse, and is a collection of various actions which occurs 
      between matter and matter (or space), in space, through time.  Sighting 
      a rifle, collapsing into a black hole, and speaking all fall under this 
      domain.

    The multiverse module itself sets a few constants, outlined in the table 
    below.

    +--------------+-----------------------------------------------------------+
    |   CONSTANT   |                          VALUE                            |
    +==============+===========================================================+
    |              | If there is no record of string ``SEED_ROOM``             |
    |  SEED_ROOM   | :class:`database <stirling.daemons.MongoDB>`, Stirling    |
    |              | assumes there is no stable multiverse, so creates a new   |
    |              | multiverse by creating a new clone of this ``SEED_ROOM``. |
    +--------------+-----------------------------------------------------------+
    | USER_SPECIES | New users are given a body belonging to this species when |
    |              | they log in for the first time.                           |
    +--------------+-----------------------------------------------------------+
"""

SEED_ROOM    = 'multiverse.space.afterlife.Entrance'
USER_SPECIES = ('multiverse.matter.organic.eukaryota.optisthokonta.metazoa.'
                'eumetazoa.bilateria.coelomata.deuterostomia.chordata.craniata.'
                'vertabrata.gnathostomata.teleostmoi.euteleostmoi.sarcoptergii.'
                'tetrapoda.amnioata.mammalia.theria.eutheria.euarchontoglires.'
                'primates.haplorrhini.simiiformes.catarrhini.hominoidea.'
                'hominidae.HomoSapien')

