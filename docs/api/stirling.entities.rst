========
Entities
========


:mod:`entities <stirling.entities>` module
******************************************

.. automodule:: stirling.entities


:class:`Entity` class
---------------------

.. autoclass:: stirling.entities.Entity
    :members: __setattr__, __getattr__, __delattr__, _set_name, 
        _get_environment, move, remove, destroy, save


:class:`Properties <stirling.entities.Properties>` class
--------------------------------------------------------

.. autoclass:: stirling.entities.Properties
    :members: __setitem__, __getitem__, __delitem__, save

:class:`NameTags <stirling.entities.NameTags>` class
----------------------------------------------------

.. autoclass:: stirling.entities.NameTags
    :members: append
