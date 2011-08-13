===================
The Stirling Engine
===================


What is Stirling?
-----------------

* 324 lines of Python.
* 538 lines of API documentation.
* 7 years of thought and preparation.
* 3 months actual work.


What does that get us?
----------------------

A multi-user multiverse simulator.


Wait, what?
-----------

.. note:: Many of the things in the follow paragraph describe features *still 
    to come*.  I wrote it this way to try and share why I am so excited about 
    this project, and why *you should be too*.

Stirling is, vaguely, a massively-multiplayer roleplaying game (MMORPG).  In 
another way, Stirling is also a simulation game akin to SimCity.  From yet 
another perspective, Stirling is more like a real-time strategy game like 
Starcraft.

How does Stirling manage to incorporate such diversity of features into a 
single game?  By giving the game engine a greater degree of freedom in how 
to manage the multiverse the game exists in, we're able to construct a much 
deeper set of instructions for how exactly things should work.

It helps to think of Stirling as a tabletop RPG, such as Dungeons & Dragons or 
Paranoia, except with the perfect Dungeon Master.  Instead of rolling the dice 
only for things occuring in the immediate vicinity of any player's characters, 
Stirling the Dungeon Master is rolling the dice for the entire dimension it is 
in charge of.  What dimension is it that Stirling is in charge of?  Whichever 
kind you build for it, and I have to brag, it is one of our goals for building 
worlds to be as easy as existing in them is.

This allows for awesome things to occur that don't normally get to happen in a 
computer game, such as evolution, climate change, the rise and fall of 
civilizations, the colonization of unsettled territory, trans-planar tourism, 
and, of course, the expansion and development of the game, just to name a few.


Okay, you have my interest.
---------------------------

Here's the bad news about all this.  I'm not the most skilled of developers to 
begin with, and my friends and I  really only work on this in my spare time.  
That means that the Stirling there is code for is not anywhere near the 
Stirling there are ideas for.


Aww.  Well, features *are* there?
---------------------------------

Unfortunately, not that many that make Stirling very useful to anyone who 
isn't a developer.  Right now, Stirling has the following features:

* A socket server for users to connect to.
* A basic API for creating simple entities.
* User registration.

And that's it.  You can't even log in again, after you've registered a user.  
Obviously, we have a way to go.  Of course, we can get there much faster with 
a few more people helping us test and develop it.


.. toctree::
    :maxdepth: 1

    /dev/index
    /api/stirling
    /glossary
    /todo
