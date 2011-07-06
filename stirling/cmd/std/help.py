import sys
import stirling
from stirling.cmd import find_cmd

def do_help(origin, cmd_name=None):
    '''
    usage: help [target]
        Target can be either a command or 'here' or 'environment'
    '''
    if cmd_name:
        if cmd_name in ['room','environment','here']:
            try:
                origin.tell(trim(origin.environment.__doc__))
                return
            except:
                origin.tell('No help for this environment')
                return
        else:
            cmd = find_cmd(cmd_name, origin.cmd_modules)
            try:
                origin.tell(getattr(cmd, 'do_%s' % (cmd_name,)).__doc__)
                return
            except:
                origin.tell('No help for this command.\n')
                return
    else:
            origin.tell(trim(__doc__))

def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed) + '\n'

