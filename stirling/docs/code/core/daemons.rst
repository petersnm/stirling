============
Core Daemons
============

There are two core daemons in Stirling, :class:`stirling.core.daemons.mud.MUDServer` and :class:`stirling.core.daemons.mud.MongoDB`; the former handles the socket server that users connect to, while the latter interfaces with our database backend.


MUDServer
=========

.. automodule:: stirling.core.daemons.mud

.. autoclass:: MUDServer
    :members: __init__, run, handle, serve_forever


MongoDB
=======

.. automodule:: stirling.core.daemons.mongodb

.. autoclass:: MongoDB
    :members: __init__, getEntity, cloneEntity, searchEntities
