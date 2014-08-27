===================
The Stirling Engine
===================


What is Stirling?
-----------------

A multi-user multiverse simulator.


What?
-----

.. note:: A lot of this description of about what I *want* Stirling to be.  
    In reality it lacks any meaningful content; a lot more work has to be 
    done on the engine first.  So take all of the below as a rough guideline 
    for where the project is heading.

The Stirling Engine is a game engine meant to manage textual multiplayer 
environments, typically known as :term:`MUDs <MUD>` (**M**\ ulti **U**\ ser 
**D**\ imension).  Instead of graphics and mouse clicks driving the world, 
it's words and written commands.::

    - gravel walkway -
    You see a white house at the end of the gravel road, with tall high 
    shrubs breaking your view on either side.
        exits: house, backward
    > smell

    There is a floral smell coming from the shrubs.

    > look at shrubs

    Covered in prickly leaves, these shrubs have small white blossoms.

    > go to house

    - outside a house -
    You're standing outside a white house.  Behind you is a gravel road, 
    with shrubs on either side.
        exits: backward

And so on, like that.  Which doesn't seem that fun, compared to modern 
video games, with their fancy graphics, HD resolutions, and so on, but! 
Without graphics, we're able to pursue a level of world dynamicism that 
simply isn't feasible with graphics.  When it's a matter of changing 
some adjectives, instead of graphic models, to make a town go from 
prosperous to poor, or to age a person, then it becomes more feasible.  
And another feature of Stirling is :term:`persistence`.  Every object 
loaded into the game world is entirely persistent.  This means that NPCs 
can grow old, have children, get sick, mountains can erode.

In recognition of the difficulties of building such a versatile and complex 
engine, we're making sure to build a solid API that is thoroughly documented.  
A big motivator for me doing this project was to enable people who don't 
program to be able to build their own game worlds.  

Dynamicism coupled with persistence, backed up by a solid API, are what will 
help Stirling be a game engine worth using.


Current Features
----------------

Right now Stirling has very few features.  In early early alpha development, 
most of the work so far is on setting up the basic structure of the engine 
so that building all that stuff I talked about up there is as easy as 
possible.  There's a socket server, a web server, an interface with MongoDB, 
and a way to register and log into user accounts.  That's about it right now.


Continued Reading
-----------------

.. toctree::
    :maxdepth: 1

    /dev/index
    /api/stirling
    /glossary
    /todo
