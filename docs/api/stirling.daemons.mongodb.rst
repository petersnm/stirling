===========
``MongoDB``
===========

The ``MongoDB`` Stirling module handles the engine's interaction with the 
external Mongo database server.  We have the daemon class :class:`MongoDB` to 
help interface with Mongo, and the two 
custom datatypes :class:`PersistList <stirling.daemons.mongodb.PersistList>` 
and :class:`PersistDict <stirling.daemons.mongodb.PersistDict>` to make saving 
dicts and lists to the database less of a hassle.

:mod:`stirling.daemons.mongodb` module
**************************************

.. automodule:: stirling.daemons.mongodb
    :show-inheritance:


:class:`MongoDB` class
----------------------

.. autoclass:: stirling.daemons.mongodb.MongoDB
    :members: get_clone, search_clones, clone_entity, make_user, get_user
    :undoc-members:
    :show-inheritance:


:class:`PersistList` class
--------------------------

.. autoclass:: stirling.daemons.mongodb.PersistList
    :members: append, remove, insert, pop
    :undoc-members:
    :show-inheritance:

:class:`PersistDict` class
--------------------------

.. autoclass:: stirling.daemons.mongodb.PersistDict
    :members: __setitem__, __delitem__
    :undoc-members:
    :show-inheritance:
