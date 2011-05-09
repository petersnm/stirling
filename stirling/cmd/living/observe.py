import stirling
import sys


def do_observe(origin, target='here', n=False, match=1):
    '''
    usage: observe -n [target]
        returns the description of the target, defaulting to current environment
        target is currently either the calling origin, their environment, or 
        anything in the calling origin's inventory or environment
        -n sets whether to render the name or not
    '''
    output = ''
    origin.debug(target)
    # These if checks determine if the player is using one of several 
    # predefined keywords.  I imagine as things get more sophisticated, this 
    # will be replaced by a search/replace of player-set nicknames.
    if target is 'here':
        observed = origin.environment
    elif target is 'me':
        observed = origin
    else:
        matches = []
        try:
            for item in origin.inventory.contents():
                if target in item.nametags:
                    matches += item
        except:
            pass
        try:
            for item in origin.environment.inventory.contents():
                if target in item.nametags:
                    matches += item
        except:
            pass
        origin.debug(matches)
        origin.debug(origin.inventory.contents())
        origin.debug(origin.environment.inventory.contents())
        if matches == []:
            origin.tell('No match found.\n')
            return
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
            pass
    origin.debug(observed)
    if n is True:
        output += '    '+observed.name+'\n'
    output += observed.desc+'\n'
    output += '('
    try:
        for item in observed.inventory.contents():
            try:
                output += item.name+', '
            except:
                pass
    except:
        pass
    output += ')\n'
    origin.tell(output)
    if output is '':
        origin.warning('Target '+target+' not found.\n')
    return
