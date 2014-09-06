"""
    .. module:: stirling.daemons.servers.http
        :synopsis: HTTP daemon and code reloader for Stirling
    .. moduleauthor:: Hunter Carroll <abzde@abzde.com>
    .. versionadded:: 0.1.1
"""

import threading
import logging
import socket
from wsgiref.simple_server import make_server

from stirling.daemons.servers.http.default_app import default

logger = logging.getLogger(__name__)

class HTTPServer(threading.Thread):
    """ HTTPServer() is a class defined to set up and run an HTTP server.  
        Stirling's HTTP server exists to create and serve pages offering 
        data about the engine's operations, while currently not providing 
        any interactive methods.
    """
    def __init__(self, addr, *a, **kw):
        """ Initialize the HTTP server.
        
            :param  addr:       A tuple of (``Host``, ``Port``)
            :type   addr:       tuple
            
            :param  \*a:        Catch-all for HTTPServer's parent's __init__
            :type   \*a:        mixed
            
            :param \*\*kw:      Additional keywords are passed to HTTPServer's
                                parent, in this case :py::class:`threading.Thread`.
            :type  \*\*kw:      mixed
            
            :returns:           None
            
            Creates a new WSGI (Web Server Gateway Interface) server bound to `addr`.
        """
        super(HTTPServer, self).__init__(*a, **kw)
        self.addr = addr
        self.logger = logger
        self.server = make_server(addr[0], addr[1], default)
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        """ HTTPServer.run() well, runs the HTTP server.
        
            :returns:           None
        """
        self.server.serve_forever()
