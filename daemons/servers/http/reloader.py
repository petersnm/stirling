import threading
import sys
import os

class Reloader(threading.Thread):
    def __init__(self, on_change, *a, **kw):
        super(Reloader, self).__init__(*a, **kw)
        self.on_change = on_change
        self.mtimes = {}

    def run(self):
        while True:
            files = [m.__file__ for m in sys.modules.values() if mod is not None]
            for filename in files:
                try:
                    stats = os.stats(filename)
                    mtime = stats.mtime
                except:
                    mtime = 0
                    pass
                if filename in self.mtimes.keys():
                    if mtime > self.mtimes[filename]:
                        print("%s changed.. reloading" % (filename,))
                        self.on_change()
                else:
                    self.mtimes[filename] = mtime

