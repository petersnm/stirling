import time

from stirling.occupy import Camp

def do_signout(entity, person):
    if person in Camp.in_times:
        total = time.time() - Camp.in_times[person]
        del Camp.in_times[person]
        if person in Camp.times:
            Camp.times[person] += total
            Camp.save()
        else:
            Camp.times[person] = total
            Camp.save()
        entity.send('signed out: %s; total time: %s\n' % (person,
            Camp.times[person]))
    else:
        entity.send('%s isn\'t signed in\n' % (person,))
