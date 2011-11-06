import time

from stirling.occupy import Camp

def do_signin(entity, person):
    Camp.in_times[person] = time.time()
    entity.send('signed in: %s\n' % (person,))

