import time

from stirling.occupy import Camp

def do_intime(entity, person):
    if person in Camp.times:
        if person in Camp.in_times:
            total = time.time() - Camp.in_times[person] + Camp.times[person]
        else:
            total = Camp.times[person]
        entity.send('%s: %s\n' % (person, total))
    elif person in Camp.in_times:
        entity.send('%s: %s\n' % (person, time.time() - Camp.in_times[person]))
    else:
        entity.send('%s has never been signed in\n' % (person,))
