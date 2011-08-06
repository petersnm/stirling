import stirling
from stirling.core.daemons.mongodb import PersistList

def animate(entity):
    entity.verbs = PersistList(self, ['standard'])
    return True

def parse(entity, message):
    if type(message) is tuple:
        if message[0] is in entity.verbs:
            pass
    pass
