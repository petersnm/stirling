'''
Part of the test suite, this is an example toothpick.
'''

from stirling.obj.object import MasterObject

class Toothpick(MasterObject):
    def __init__(self, **kw):
        super(Toothpick, self).__init__(**kw)

    def new():
        self.name = 'toothpick'
        self.desc = ('A small sliver of pale wood, about two inches long.')
