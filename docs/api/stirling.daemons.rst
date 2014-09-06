=======
Daemons
=======

Within Stirling, :term:`daemons <daemon>` act in the background, handling 
complex interactions between entities and interactions between Stirling and the 
external system (such as the MongoDB server.)

There are currently two daemons which **must** be instanced and running for 
the rest of Stirling to operate.  The first daemon, :class:`MongoDB 
<stirling.daemons.mongodb.MongoDB>`, handles the interfacing between Stirling 
interacts with the external Mongo database server, which is required for 
entities to be :term:`cloned <clone>` into the :term:`multiverse`.  The second, 
:class:`MUDServer <stirling.daemons.server.mud.MUDServer>`, runs a socket 
server to handle incoming user connections and send them MUD-style output.

.. note:: Daemons are usually instanced upon the initialization, and this 
  instance is what is used across the engine.  For example, in order to use 
  the :class:`MongoDB <stirling.daemon.mongodb>` daemon to make a user, you 
  would use ``stirling.daemons.Mongo.make_user()``.  This convention and 
  others are more thoroughly explained in the :doc:`Developer Handbook 
  </dev/index>`.

.. todo:: Add a HTTP server to act as alternative way of interacting with 
  - the engine.

Submodules
**********

.. toctree::
    :maxdepth: 1

    stirling.daemons.mongodb
    stirling.daemons.servers

:mod:`stirling.daemons` module
********************************

.. automodule:: stirling.daemons.__init__
