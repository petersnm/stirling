"""
/lib/living.py
emsenn@Stirling
190411

The master object of the MUD, all objects inherit it at some point
"""

import sys

from stirling.obj.object import MasterObject
from stirling.cmd import find_cmd

class Living(MasterObject):
    def __init__(self, **kw):
        super(Living, self).__init__(**kw)
        self.exclude += ['parse_lines']
        self.cmd_modules = ['cmd']

    def parse_line(self, line):
        cmd = False
        words = line.split()
        if len(words) == 0:
            return False
        cmd_name = words[0]
        try:
            args = words[1:]
        except:
            args = None
        cmd = find_cmd(cmd_name, self.cmd_modules)
        if not cmd:
            self.tell('No such command: %s\n' % (cmd_name,))
            return False
        try:
            if args is not None:
                kwargs = {}
                normarg = ''
                substr = None
                subname = ''
                subtype = 0 # none
                for arg in args:
                    if substr is not None:
                        if subtype == 1:
                            if arg.endswith('"'):
                                if len(arg) < 1:
                                    substr = substr + ' '
                                else:
                                    substr = substr + ' ' + arg[:-1]
                                kwargs[subname] = substr    
                                subname = ''
                                substr = None
                            else:
                                substr = substr +' ' + arg
                        elif subtype == 2:
                            substr += ' ' + arg
                    else:
                        if arg.startswith('--'):
                            name, value = arg[2:].split('=')
                            kwargs[name] = value
                            if value.startswith('"'):
                                if value.endswith('"'):
                                    if len(value) < 3:
                                        kwargs[name] = ''
                                    else:
                                        kwargs[name] = value[1:-1]
                                else:
                                    substr = value[1:]
                                    subtype = 1 # kw sub
                                    subname = name
                        elif arg.startswith('-'):
                            for name in arg[1:]:
                                kwargs[name] = True
                        else:
                            substr = arg
                            subtype = 2
            if substr is not None:
                return getattr(cmd, 'do_%s' % (cmd_name,))(self, substr, **kwargs)
            else:
                return getattr(cmd, 'do_%s' % (cmd_name,))(self, **kwargs)

        except TypeError:
            self.tell('Too many/few arguments to given to %s\n' % (cmd_name,))
            return False
        except:
            pass
            return False
