import threading
import sys
import os
import logging
import imp
import stirling.www

class HTTPReloader(threading.Thread):
    def __init__(self, http_server, *a, **kw):
        super(HTTPReloader, self).__init__(*a, **kw)
        self.logger = logging.getLogger(self.__module__)
        self.mtimes = {}
        self.http_server = http_server
        self.running = True
        self.mods = {}

    def run(self):
        while self.running:
            self.mods.update(sys.modules)
            for name, module in self.mods.items():
                if hasattr(module, '__file__'):
                    try:
                        stat = os.stat(module.__file__)
                        mtime = stat.st_mtime
                    except:
                        mtime = 0
                    if module.__file__ in self.mtimes.keys():
                        if mtime > self.mtimes[module.__file__]:
                            self.logger.info('reloading.. (%s)' % (name,))
                            sys.modules[name] = imp.reload(module)
                            sys.modules['stirling.daemons.servers.http'] = \
                                imp.reload(sys.modules['stirling.daemons.servers.http'])
                            sys.modules['stirling.www'] = \
                                imp.reload(sys.modules['stirling.www'])
                            stirling.www.start()
                            self.http_server.server.shutdown()
                            self.running = False
                            break
                    else:
                        self.mtimes[module.__file__] = mtime
