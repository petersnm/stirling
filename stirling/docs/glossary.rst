========
Glossary
========

A list of all the terms that Stirling uses in a specific way.

.. glossary::

    adjective
        Any :term:`entity` may have a variety of adjectives associated with 
        it, which are used to help distinguished it based on its physical 
        :term:`properties`.  A baker may have the adjectives  ``['fat', 
        'male', 'tall']``.

    daemon
        A daemon within the scope of Stirling is similar to a daemon in the 
        \*nix world.  Typically running from the time the server is 
        intitialized, daemons do the global or timed events that the game 
        needs to happen in order to keep working.  
        :class:`stirling.core.daemons.mongodb.MongoDB` is a good example of 
        what a daemon can be.

    entity
        In Stirling, an entity is any thing within the game universe which has 
        quantifiable physical :term:`properties`.  Anything from a beam of 
        light to your mother could be represented as an entity within 
        Stirling.  An important thing to note about entities are the fact that 
        they are persistent.  Any property that an entity holds, it will 
        continue to hold, through reboots or crashes.  This is what gives 
        Stirling our unique ability to do such long-term and dynamic things 
        with our universe.

    nametag
        An :term:`entity` has a list of nametags, which are all the nouns that 
        may be used to refer to the object.  A baker may have the nametags 
        ``['baker','steve','man','human','entity','thing']``

    properties
        The physical attributes of an :term:`entity`.
