""" The daemons that Stirling needs to run.

    .. module: stirling.daemons

    .. modauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded: 0.1

    `Daemons` within Stirling are similar to daemons within the \*nix world.  
    For a full explanation of what a daemon is, I recommend reading the 
    :term:`glossary entry <daemon>` on them.

    There are two daemons that Stirling must have running in order to operate; 
    :class:`the MUDServer <stirling.daemons.mud.MUDServer>` and 
    :class:`MongoDB <stirling.daemons.mongodb.MongoDB>`.

    
"""

from stirling.daemons.mongodb import MongoDB
from stirling.daemons.mud import MUDServer
