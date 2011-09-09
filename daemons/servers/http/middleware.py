import traceback
import re
import logging

class RequestWare():
    def __init__(self, app):
        self.logger = logging.getLogger(self.__module__)
        self.app = app

    def __call__(self, env, start_response):
        try:
            req = Request(self, env)
            res = self.app(req)
            start_response('200 OK', [('content-type', 'text/html')])
            if type(res) is str:
                return [res.encode('utf-8')]
            else:
                return res
        except:
            start_response('500 Error', [('content-type', 'text/plain')])
            return [traceback.format_exc().encode('utf-8')]

class Request(object):
    def __init__(self, app, env):
        self.logger = app.logger
        self.app = app
        self.env = env
        self.path = env['PATH_INFO']

    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            if attr in self.env:
                return self.env[attr]        
            elif attr.upper() in self.env:
                return self.env[attr.upper()]
            else:
                raise 

class App:
    def __init__(self):
        self.url_patterns = []
        
    def __call__(self, req):
        for pattern, func in self.url_patterns:
            if pattern.match(req.path):
                # shorten req.path here #
                return func(req)
        else:
            return "oh noes! 404z!"
            
    @staticmethod        
    def url(pattern):
        def _inner_url(func):
            self.url_patterns.append((pattern, func))
            return func
        return _inner_url

