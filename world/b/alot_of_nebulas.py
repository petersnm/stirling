import stirling
from stirling.obj.living import Living

class Alot(Living, **kw):
    def __init__(**kw):
        super(Alot, self).__init__(**kw)
        self.name = 'alot of nebulas'
        self.desc = ('This alot of nebulas doesn\'t look quite right in the '
          'head.  It had dark matter frothing from its celestial jowls, and '
          'it menaces with spikes of gamma radiation.')
