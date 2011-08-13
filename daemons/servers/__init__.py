""" The serving daemons of Stirling.

    .. module:: stirling.daemons.server
        :synopsis: Daemons which serve information externally.
    .. moduleauthor:: Morgan Sennhauser <emsenn@emsenn.com>
    .. versionadded:: 0.1

    This module includes the :term:`daemons <daemon>` which serve information 
    to external services and users.  At the moment, the only serving daemon 
    is the MUD server; the socket server which users connect to to receive 
    the textual output of the engine.

    .. todo:: We need an HTTP serving daemon
"""
import stirling
from stirling.daemons.servers.mud import MUDServer

MUD = MUDServer((stirling.HOST, stirling.MUD_PORT))
