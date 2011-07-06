'''
/world/dev/room/alot_of_yetis.py
emsenn@Stirling
280411

Part of the test suite, this is an alot.
'''

from stirling.obj.living import NPC

class Seirou(NPC):
    def __init__(self, **kw):
        super(Alot, self).__init__(**kw)

    def new():
        self.name = 'Seirou'
        self.desc = ('This alot named Seirou has over 25 years of winking '
          'experience.  ;)')
