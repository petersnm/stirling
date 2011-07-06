import stirling

def do_test3(origin, *a, **kw):
    foo = stirling.clone('world.dev.obj.toothpick.Toothpick')
    foo.move(origin.environment)
