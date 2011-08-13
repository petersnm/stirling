==============
The MUD Server
==============

The main method of receiving output from the Stirling engine is by connecting 
to the :class:`MUDServer`.  Based on a socket server, the MUD server daemon 
handles the textual output of the engine, sending caught text from a user's 
:term:`entity` to their socket connection, and passing commands from the user's 
connection to their entity.


:mod:`stirling.daemons.servers.mud` module
******************************************

.. automodule:: stirling.daemons.servers.mud


:class:`MUDServer` daemon
*************************

.. autoclass:: stirling.daemons.servers.mud.MUDServer
    :members: run, handle, register_user, login_user, tutorial, disconnect
    :undoc-members:
    :show-inheritance:
