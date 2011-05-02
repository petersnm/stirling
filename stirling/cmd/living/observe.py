from stirling.daemon.objects import get_object

def do_observe(obj, target='here', v=False, t=False, s=False, n=False):
    '''
    usage: observe -n [target]
        returns the description of the target, defaulting to current environment
        target is currently either the calling object, their environment, or 
        anything in the calling object's inventory or environment
        -n sets whether to render the name or not
    '''
    obj.debug(obj.properties)
    output = ''
    if target in ['room','here','environment']:
        if n is True:
            output += '['+obj.environment.name+']\n'
        output += get_object(obj.environment).desc+'\n'
    elif target in ['self','me',obj.name]:
        if n is True:
            output += '['+obj.name+']\n'
        output += obj.desc+'\n'
    else:
        for item in obj.environment.inventory+obj.inventory:
            if target in item.nametags:
                if n is True:
                    output += '['+item.name+']\n'
                output += item.desc+'\n'
    obj.tell(output)
    if output is '':
        obj.warning('Target '+target+' not found.\n')
    return
