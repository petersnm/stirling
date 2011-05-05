def do_test(obj, *a, **kw):
    '''
    usage: test [boolean] [kv] [target]
        All purpose test command, use it for whatever you need
    '''
    obj.environment.name = 'moose'
    obj.environment.save()
    obj.tell('test')
