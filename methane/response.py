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

