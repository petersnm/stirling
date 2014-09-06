===================
Developers Handbook
===================

Your ultimate guide to building anything with Stirling!


Getting Started
---------------

First off, this guidebook assumes you aren't a programmer, so might be a 
bit (or a lot) more verbose than you need.  It does assume you're able to 
google terms you might not know, though anything that's used in a Stirling-
specific way should be defined in our :doc:`/glossary`.  It also assumes 
that you're working with us, on the main development branch of the project.  
This is hosted on `GitHub <http://github.com/emsenn/stirling>`_, where you 
can take a look at the code.  This documentation is hosted at 
`emsenn.net <http://emsenn.net/stirling/>`_  There aren't any real commitments 
to being a developer for Stirling.  The basics are: set up your own Stirling
engine, make your changes, and submit it to the main development branch.  
Changes, here, can be either new code, or revisions to existing code.  It's 
recommended you learn how to build some simple objects and 
:term:`rooms <room>`.  Once you're adept at that, you could start making 
:term:`actions <action>`, or help 
`fix bugs <http://github.com/emsenn/stirling/issues>`_.  By then, you should 
have a thorough knowledge of Stirling's API, so why not make a fork of the 
project, and make your own game world?


Prerequisites
=============

Before you can start doing any development, you have to get your own copy 
of Stirling, and get it running.  In order to participate with the other 
developers, you'll also need to make an account on GitHub.

There are a few prerequisite software packages you'll need on your system 
for Stirling to run.

* **Linux**.  While Stirling may work on OSX and Windows, we don't support it.
* **Python 3.4**.  Again, Stirling might work with another version, but we 
  won't support it.
* **MongoDB**.  And the appropriate Python module, :py:mod:`pymongo`.
* **Git**.  You'll need this to track your changes so that other developers 
  can get an idea of what you've done.
* **PyLint**.  Also not necessary, but Stirling requires all code added 
  to the master branch conform to PEP8, so unless you want your changes 
  denied for petty reasons...

The installation and setup of these packages is beyond the scope of this 
documentation.  Please see the website of each package for that information.  
Once everything is installed, make sure Git is set up and start the MongoDB
system daemon.

Installing Stirling
===================

You can fetch the git repository to your system with the shell command 
``git clone git://github.com/emsenn/stirling.git``.  Looking in the 
main directory, you'll see several files.  The first one you'll want to 
change is ``__init__``.  You can change some global variables (like 
port number) if you need to.  After that, execute ``run_engine.py``.  If 
it doesn't work, search for your error on our 
`issues page <http://github.com/emsenn/stirling/issues>`_, and if it appears 
to be unique, go ahead and file an issue.

If it appears to have worked, go ahead and try and connect to the MUD via 
telnet, or your MUD client of choice.  You should see a screen that looks 
something like this::

    [emsenn@ack stirling]$ telnet localhost 5878
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    Stirling
    0.1.1
        What the what

    Stirling is a engine for building textual MMORPGs, and is currently 
    in really really really early development.  So unless you're a developer, 
    there is not much here for you to do.  If you are a developer, you 
    probably don't even read this message anymore, and won't notice that 
    I've changed it for quite some time.  For more information, check out 
    http://github.com/emsenn/stirling/
    Please enter your [desired] username.
    >

You can go ahead and enter a username and password if you want, and then go 
ahead and log back out.  Before we start diving into development, let's 
go over some fundamentals of how Stirling works.

Multiverse Mechanics
--------------------

Stirling exists to simulate a :term:`multiverse`.  Within the scope of 
Stirling, a multiverse has four domains.

* **Space** is a collection of the physical locations within the multiverse.  
  Each location may be of arbitrary size, representing whatever scope of 
  space is appropriate.  The main module is :mod:`stirling.multiverse.space`.  
  Each unit of space is called a :term:`room`, because that's a convenient 
  way of thinking about them.
* **Time** is the generally refers to what is tracked by the 
  :class:`stirling.multiverse.time.Ticker()` daemon, but includes everything 
  in the :mod:`stirling.multiverse.time` module.  The time stuff has not 
  been written yet, but will use a global ticker to queue and execute any 
  command any entities or daemons need executed.  For the extra-geeky, 
  a bucketed batched phased update daemon.
* **Matter** is the hierarchical catalog of all the entities that can be 
  instanced inside of the multiverse.  Its main entity is 
  :class:`stirling.multiverse.matter.Matter`.
* **Energy** is the collection of actions which commonly occcur between 
  entities of matter, or that entities can do to a room.  Pretty much 
  just think of them as just sets of instructions for helping entities 
  interact.

Through these four domains, we should be able to simulate the bulk of what 
we need to, to make the kind of game engine I'm aiming for.

Space
=====


Time
====


Matter
======


Energy
======


The Stirling API
----------------
