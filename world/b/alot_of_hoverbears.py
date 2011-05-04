'''
/world/dev/room/alot_of_hoverbears.py
ploosk@Stirling
040511

Part of the test suite, this is an alot.
'''

from stirling.obj.living.npc import NPC

class Alot(NPC):
    def __init__(self):
        super(Alot, self).__init__()
        self.set_name('alot of hoverbears')
        self.set_desc('This large, floating ball is made entirely of '
          'hoverbears. It produces a low humming noise as it levitates.')
