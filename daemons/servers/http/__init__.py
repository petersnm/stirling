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

from stirling.daemons.servers.http.reloader import HTTPReloader

logger = logging.getLogger(__name__)

class ReloadingHTTPServer(threading.Thread):
    """ The ReloadingHTTPServer wrapper around the :class:`HTTP reloader
        <stirling.dameons.servers.http.reloader.HTTPReloader>` and the
        :class:`HTTP server <stirling.daemons.servers.http.HTTPServer>`
    """
    def __init__(self, addr, *a, **kw):
        """ Initializes the main thread and and stores the bind address and a
            the logger
            
            :param  addr:       A tuple of (``Host``, ``Port``).
            :type   addr:       tuple

            :param \*a:         Any additional arguments are passed to the
                                  parent
            :type \*a:          mixed

            :param  \*\*kw:     Any additional keywords are passed to the 
                                  parent, in this case, 
                                  :py::class:`threading.Thread`.
            :type   \*\*kw:     mixed

        """
        super(ReloadingHTTPServer, self).__init__(*a, **kw)
        self.addr = addr
        self.logger = logger

    def run(self):
        while True:
            self.http_server = HTTPServer(self.addr)
            self.reloader = HTTPReloader(self.http_server)
            self.logger.info('spawning http reloader and server')
            self.reloader.start()
            self.http_server.start()
            self.http_server.join()
            self.reloader.join()
            del self.http_server
            del self.reloader

class HTTPServer(threading.Thread):
    def __init__(self, addr, *a, **kw):
        super(HTTPServer, self).__init__(*a, **kw)
        self.addr = addr
        self.logger = logger
        from stirling.daemons.servers.http.middleware import StirlingWare
        self.server = make_server(addr[0], addr[1], StirlingWare(lambda x: "foo"))
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                1)

    def run(self):
        self.server.serve_forever()
