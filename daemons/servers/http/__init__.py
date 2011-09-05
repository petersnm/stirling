import threading
import logging
from wsgiref.simple_server import make_server

from stirling.daemons.servers.http.app import app

class HTTPServer(threading.Thread):
    def __init__(self, addr, *a, **kw):
        super(HTTPServer, self).__init__(*a, **kw)
        self.addr = addr
        self.log = logging.getLogger(self.__module__)
        self.server = make_server(addr[0], addr[1], app)
    
    def run(self):
        self.server.serve_forever()

