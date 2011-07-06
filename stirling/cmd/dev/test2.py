import stirling

def do_test2(obj, *a, **kw):
    '''
    usage: test2 [boolean] [kv] [target]
        All purpose test command, use it for whatever you need
    '''
    try:
        foo = stirling.clone('world.dev.obj.toothpick.Toothpick')
        obj.debug(foo)
        foo.move(obj.environment)
    except:
        obj.debug(moose)
    return
