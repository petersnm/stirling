import stirling
import sys

def do_clone(origin, target='', h=False):
    origin.debug('foo')
    try:
        cloned = stirling.clone(target)
        origin.debug(cloned)
        if h is True:
            cloned.move(origin.environment)
    except:
        origin.debug(sys.exc_info())
    return
