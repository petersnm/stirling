========================================
The Developer's Introduction to Stirling
========================================

This project has always been ambitious. From the beginning, way back in 2004, the development team had lofty goals. We wanted a fully dynamic MUD, one that adapted to the players actions. Cities and empires would rise and fall overnight. It would truly be a feat of programming. It ultimately fizzled and faded away. What we were trying to do was near impossible on the codebase we chose. We tried many different codebases, all failed through being awkward to work with or so outdated. So we gave up for a time.
Now, the project is back. We've written an entirely new engine in Python from the ground up, using modern technologies. These articles will describe the engine and why as a developer, you would want to use it. 

What is the Stirling engine?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Stirling engine was a heat based engine designed in the early 1800's to replace the steam engine. It was quieter, safer, and more efficient. It never took hold because the steam engine was already there. Our stirling engine codebase is a similiar concept. We've written it to be faster, newer, and far more efficient. We see so many text based games still using the same engines that were made in the 90's! Our engine is a modern take on an old concept, one with improvements for a modern coding environment.

Why the Stirling engine?
~~~~~~~~~~~~~~~~~~~~~~~~
The main question to ask is, why should I use the Stirling engine when there are other established alternatives like LPC available? 
Stirling is written in Python. That means its runnable *without mucking around in compilers* on any computer that has a python install. That means basically every computer. Because it's written in Python, it's easily extendible using the huge number of ready-made extensions available to python users. Furthermore, the basic core that comes with python does much, much more than any Diku or LPC mud. Second, the entire engine is persistant. If your server goes down for any reason, the entire game can be brought back up exactly how it was. We accomplish this using the MongoDB. Persistance is hard-wired our master class, the entity. Everything in the engine has it. But wait, there's more. Stirling is designed to emulate a world as closely a possible. Every entity has the ability to do certain tasks. To make something lifelike, you simply create its description and choose a series of tasks for it to inherit.  

