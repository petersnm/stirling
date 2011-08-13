================
The Stirling API
================

Stirling is a `Python3 <http://docs.python.org/release/3.0.1/index.html>`_ 
software package providing an API for creating and operating simulated 
:term:`multiverses <multiverse>`.  Our goal is not to be a precise emulation of 
anything, but an accurate simulation of everything.

.. note:: While Stirling is designed around building :term:`MMORPGs <MUD>`, the 
  code and documentation is written for more general simulation software, which 
  is explained below.
  

To accomplish this, we had to look at how reality works, which parts were 
important to incorporate into the engine, and how to organize them in a way 
that will make it easy for other developers (such as yourself) to use them.  
After far too long (about seven years) of contemplating, attempting, and 
failing, we have finally settled on just how to accomplish recreating all of 
existence in a comprehensible software package.

Almost everything within Stirling falls into one of two categories:

* **Entities** make up most of the multiverse.  Anything with quantifiable 
  physical presence is an :term:`entity` - a laser beam, a sword, or your 
  mother could all be entities.  Any entity which exists within the multiverse 
  (explained two bullet points down) is persistently stored using `MongoDB 
  <http://www.mongodb.org>`_ and `PyMongo 
  <http://api.mongodb.org/python/current/>`_.  This means that in the event 
  of a shutdown (expected or not), entities return with the exact set of 
  attributes with the same values.  This allows us to do a lot of things 
  which traditional game engines cannot, such as an :term:`NPC` baker 
  increasing his skills, falling in love, getting sick, having kids, and so 
  on.  The :class:`Entity <stirling.entities.Entity>` class explains how 
  persistence works and may be applied a bit more thoroughly.

* **Daemons** are what make Stirling do anything.  Handling most complex 
  interactions between entities, as well as interactions between Stirling and 
  the external world, :term:`daemons <daemon>` run things such as the 
  :class:`database <stirling.daemons.mongodb.MongoDB>`, weather, and the 
  economy.  Daemons typically are **not** persistently stored in the database, 
  although some may store a few attributes.

These two types of objects cooperate to represent and manage the 
:mod:`multiverse <stirling.multiverse>`, the collection of entities which 
comprise the game world.  The multiverse itself is split into four submodules, 

    * :mod:`Space <stirling.multiverse.space>` is the collection of all 
      :term:`rooms <room>` on the MUD; static environments that do not really 
      change location relative to the multiverse as a whole.

    * :mod:`Time <stirling.multiverse.time>` is a daemon and related functions 
      for controlling the fourth dimension.

    * :mod:`Matter <stirling.multiverse.matter>` is the hierarchical catalog of 
      entities which exist within space.

    * :mod:`Energy <stirling.multiverse.energy>` is the collection of actions, 
      which occur between matter (or space), in space, through time.

You may note this is identical to the four divisions of the universe typically 
used by scientists.  This is intentional; in order to make Stirling's API 
easy to learn and apply, we often model our modules after scientific theories.

Below is a list of links to the Stirling's main submodules' API documentation, 
and below that is the documentation for Stirling's main module, :mod:`stirling`.


Submodules
**********

.. toctree::
    :maxdepth: 1

    stirling.daemons
    stirling.entities
    stirling.multiverse


:mod:`stirling` module
**********************

.. automodule:: stirling.__init__


:class:`BaseObj` class
----------------------

.. autoclass:: stirling.BaseObj
    :members: debug, info, warning, error
    :undoc-members:
    :show-inheritance:
