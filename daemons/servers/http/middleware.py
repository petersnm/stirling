import traceback
import re
import logging

class StirlingWare():
    def __init__(self, dispatch_rules=[]):
        self.dispatcher = Dispatcher(dispatch_rules)
        self.logger = logging.getLogger(self.__module__)

    def __call__(self, env, start_response):
        try:
            req = Request(self, env)
            rules = []
            res = self.dispatcher(req)
            if type(res) is str:
                start_response('200 OK', [('content-type', 'text/html')])
                return [res.encode('utf-8')]
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

class Dispatcher():
    def __init__(self, rules=[]):
        self.rules = []
        for rule, func in rules:
            self.rules.append((re.compile(rule), func))
    
    def add_rule(self, rule, func):
        self.rules.append((re.compile(rule), func))
    
    def bind(self, rule):
        def _inner_bind(func):
            self.rules.append((re.compile(rule), func))
        return _inner_bind
    
    def __call__(self, req):
        for rule, func in self.rules:
            match = rule.match(req.path)
            if rule.match(req.path): 
                req.path = req.path[match.end()-1:]
                return func(req)
        else:
            return "404"
