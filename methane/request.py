class Request(object):
    def __init__(self, env, start_response):
        self.env = env
        self.start_response = start_response
        self.path = env['PATH_INFO']       

