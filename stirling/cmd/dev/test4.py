import stirling

def do_test4(origin, *a, **kw):
    foo = origin.environment.inventory
    for item in foo:
        i = stirling.get(item)
        print(i)
        if type(i) != dict:
            if i.name == 'toothpick':
                i.destroy()

