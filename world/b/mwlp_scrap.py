'''
Mysterious Scrap Of Paper
'''

from stirling.obj.object import MasterObject

class MWLPScrap(MasterObject):
    def __init__(self):
        super(MWLPScrap, self).__init__()
        self.set_name('scrap of paper')
        self.set_desc('This is a small scrap of paper, with the letters "MWLP" '
          'written on it, and a drawing of what appears to be a bearded man '
          'holding a futuristic-looking pistol')
