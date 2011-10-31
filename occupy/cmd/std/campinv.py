from stirling.occupy import Camp

def do_campinv(entity, *a, action='list', s=False, g=False):
    if action is 'set' or s:
        Camp.count_inv[' '.join(a[1:])] = a[0]
        Camp.save()
    elif action is 'get' or g:
        entity.send("%s: %s\n" % (' '.join(a), Camp.count_inv[' '.join(a)]))
    else:
        entity.send("inventory: %s\n" % (Camp.count_inv,))

