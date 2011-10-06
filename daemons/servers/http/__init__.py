"""
    .. module:: stirling.daemons.servers.http
        :synopsis: HTTP daemon and code reloader for Stirling
    .. moduleauthor:: Hunter Carroll <abzde@abzde.com>
    .. versionadded:: 0.2
"""

import threading
import logging
import socket
from wsgiref.simple_server import make_server

from stirling.daemons.servers.http.default_app import default

logger = logging.getLogger(__name__)

class HTTPServer(threading.Thread):
    def __init__(self, addr, *a, **kw):
        super(HTTPServer, self).__init__(*a, **kw)
        self.addr = addr
        self.logger = logger
        self.server = make_server(addr[0], addr[1], default)
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.server.serve_forever()
