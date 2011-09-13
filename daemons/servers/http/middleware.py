import re
import traceback
import logging

class App:
    def __init__(self, name):
        self.name = name
        self.url_patterns = []
        
    def __call__(self, env, start_response):
        try:
            req = Request(env, start_response)
            for pattern, func in self.url_patterns:
                if pattern.match(req.path):
                    # shorten req.path here #
                    res = func(req)
                    break
            else:
                res = Response('404 Not Found', {'content-type': 'text/plain'}, 'four oh four error\nthat url was not found\ndid you type it wrong?')
            if type(res) is not Response:
                res = Response(body=res)
            ret = res.respond(start_response)
            del req
            del res
            return ret
        except:
            start_response('500 fffffffuuuuuuuuuuuu', [('content-type', 'text/plain')])
            return [traceback.format_exc().encode('utf-8')]
        
    def url(self, pattern):
        def _inner_url(func):
            self.url_patterns.append((re.compile(pattern), func))
            return func
        return _inner_url

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
