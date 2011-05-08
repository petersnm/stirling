import sys 
import stirling


def do_observe(origin, target='here', n=False, match=1):
    '''
    usage: observe -n [target]
        returns the description of the target, defaulting to current environment
        target is currently either the calling originect, their environment, or 
        anything in the calling originect's inventory or environment
        -n sets whether to render the name or not
    '''
    output = ''
    # These if checks determine if the player is using one of several 
    # predefined keywords.  I imagine as things get more sophisticated, this 
    # will be replaced by a search/replace of player-set nicknames.
    if target in ['room','here','environment']:
        observed = origin.environment
    elif target in ['self','me']:
        observed = origin
    else:
        matches = []
        try:
            for item in origin.inventory.contents():
                if target in item.nametags:
                    matches += item
        except:
            origin.debug(sys.exc_info())
        try:
            for item in origin.environment.inventory.contents():
                if target in item.nametags:
                    matches += item
        except:
            origin.debug(sys.exc_info())
        origin.debug(matches)
        try:
            if match is not 1:
                if len(matches) is not 1:
                    observed = matches[match] 
                else:
                    origin.tell('Only one match for \''+target+'\', using it.')
                    observed = matches[0]
            else:
                observed = matches[0]
        except:
            origin.debug(sys.exc_info())
    if n is True:
        output += '    '+observed.name+'\n'
    output += observed.desc+'\n'
    output += '('
    for item in observed.inventory.contents():
        output += item.name+', '
    output += ')\n'
    origin.tell(output)
    if output is '':
        origin.warning('Target '+target+' not found.\n')
    return
