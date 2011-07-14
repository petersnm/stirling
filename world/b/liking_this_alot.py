import stirling
from stirling.obj.living import Living

class Alot(Living, **kw):
    # https://plus.google.com/113208553012122994072/posts/Ta4Zq5nAk7C
    def __init__(**kw):
        super(Alot, self).__init__(**kw)
        self.name = 'friendly alot'
        self.desc = ('This alot seems very kind and friendly, in fact, you '
          'like this alot.')
