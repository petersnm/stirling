'''
Part of the test suite, this is an example toothpick.
'''

from stirling.obj.object import MasterObject

class Toothpick(MasterObject):
    def new():
        super(Toothpick, self).new()
        self.debug('new\'d')
        self.name = 'toothpick'
        self.desc = ('A small sliver of pale wood, about two inches long.')
