""" Daemons control interactions between entities, and handle processes 
    not suitable for entities.

    .. module: stirling.daemons
        :synopsis: Imports and instances critical daemons.
    .. modauthor: emsenn <morgan.sennhauser@gmail.com>
    .. versionadded: 0.1.1

    This module imports and instances critical daemons.  At the moment this 
    is only the MongoDB daemon.

    :var    Mongo:      an instance of :class:`MongoDB <stirling.daemons.mongodb>`
"""

from stirling.daemons.mongodb import MongoDB

Mongo = MongoDB()

