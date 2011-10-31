from stirling.entities import Entity

class Camp(Entity):
    def __init__(self, *a, **kw):
        Entity.__init__(self, *a, **kw)
        self.count_inv = {}

