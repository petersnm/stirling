import stirling
import sys


def do_observe(obj, target='here', v=False, t=False, s=False, n=False):
    '''
    usage: observe -n [target]
        returns the description of the target, defaulting to current environment
        target is currently either the calling object, their environment, or 
        anything in the calling object's inventory or environment
        -n sets whether to render the name or not
    '''
    output = ''
    if target in ['room','here','environment']:
        viewed = obj.environment
        if n is True:
            output += '['+viewed.name+']\n'
        output += viewed.desc+'\n'
        output += '('
        for item in viewed.inventory.contents():
            try:
                output += item.name+', '
            except:
                # temp fix until players despawn and shit in a sane way.
                pass
        output += ')\n'
    elif target in ['self','me',obj.name]:
        viewed = obj
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
