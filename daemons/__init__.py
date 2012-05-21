""" Daemons control the complex interactions between :term:`entities <entity>`.

    .. module: stirling.daemons
    .. modauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded: 0.1

    This module imports and creates an instance of :class:`MongoDB 
    <stirling.daemons.mongodb>` named ``stirling.daemons.Mongo``.  At the 
    moment, this is the only thing the main daemon module does, mostly because 
    so far, the MongoDB daemon is our only non-server daemon!
"""

from stirling.daemons.mongodb import MongoDB

Mongo = MongoDB()

