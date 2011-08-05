""" The core daemons that Stirling needs to run.

    .. module: stirling.core.daemons

    .. modauthor: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded: 0.1

    `Daemons` within Stirling are similar to daemons within the \*nix world.  
    For a full explanation of what a daemon is, I recommend reading the 
    :term:`glossary entry <daemon>` on them.

    There are two daemons that Stirling must have running in order to operate; 
    :class:`the MUDServer <stirling.core.daemons.mud.MUDServer>` and 
    :class:`MongoDB <stirling.core.daemons.mongodb.MongoDB>`.

    
"""

from stirling.core.daemons.mongodb import MongoDB
from stirling.core.daemons.mud import MUDServer
