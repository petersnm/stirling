import sys

import stirling


def do_say(origin, target=''):
    '''
    usage: say [statement]
        Writes the statement to the room as though the player has said it.
    '''
    if target == '':
        origin.tell('Say what?')
        return
    i = [item for item in origin.environment.inventory.contents() 
      if item is not origin]
    for item in i:
        item.tell(origin.name+' says, "'+target+'"\n')
    origin.tell('You say, "'+target+'"\n')
    return
