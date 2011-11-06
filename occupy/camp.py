from stirling.entities import Entity

class Camp(Entity):
    def initialize(self):
        Entity.initialize(self)
        self.count_inv = {}
        self.in_times = {}
        self.times = {}
