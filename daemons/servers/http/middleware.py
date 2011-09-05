import traceback

class StirlingWare():
    def __init__(self, app):
        self._inner_app = app
        self.dispatcher = Dispatcher(self)

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
        self.app = app
        self.env = env

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
    def __init__(self, app, rules=[]):
        self.app = app
        self.rules = rules

    def __call__(self, req):
        return "dispatch-fu!"
