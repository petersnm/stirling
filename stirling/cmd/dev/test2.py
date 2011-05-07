import stirling

def do_test2(obj, *a, **kw):
    '''
    usage: test2 [boolean] [kv] [target]
        All purpose test command, use it for whatever you need
    '''
    foo = stirling.clone('world.dev.obj.toothpick.Toothpick')
    foo.move(obj.environment)
