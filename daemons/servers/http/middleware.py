import re
import traceback
import logging

class App:
    def __init__(self, name):
        self.name = name
        self.url_patterns = []
        
    def __call__(self, env=None, start_response=None, req=None, **kw):
        try:
            if req is None:
                req = Request(env, start_response)
            for pattern, call in self.url_patterns:
                match = pattern.match(req.path)
                if not hasattr(req, 'consumed_path'):
                    req.consumed_path = req.path
                if match:
                    # shorten req.path here
                    kw.update(match.groupdict())
                    req.consumed_path = req.consumed_path[match.end():]
                    res = call(req=req, **kw)
                    break
            else:
                res = Response(
                    '404 Not Found', 
                    {'content-type': 'text/plain'}, 
                    'four oh four error\nthat url was not found\ndid you type it wrong?',
                )
            if type(res) is not Response:
                res = Response(body=res)
            if env is None and start_response is None:
                return res
            ret = res.respond(req.start_response)
            del req
            del res
            return ret
        except:
            start_response('500 fffffffuuuuuuuuuuuu', [('content-type', 'text/plain')])
            return [traceback.format_exc().encode('utf-8')]
        
    def url(self, pattern):
        def _inner_url(call):
            self.url_patterns.append((re.compile(pattern), call))
            return call
        return _inner_url

    def bind(self, pattern, call):
        self.url_patterns.append((re.compile(pattern), call))

class Request(object):
    def __init__(self, env, start_response):
        self.env = env
        self.start_response = start_response
        self.path = env['PATH_INFO']       

class Response(object):
    def __init__(self, status='200 OK', headers={'content-type': 'text/plain'}, body=[]):
        self.status = status
        self.headers = headers
        if type(body) is str: self.body = [body.encode('utf-8')]
        else: self.body = body
        
    def respond(self, start_response):
        self.headers['content-length'] = str(len(b'\n'.join(self.body)))
        start_response(self.status, list(self.headers.items()))
        return self.body
