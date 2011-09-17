from methane import App

demo = App('demo')

@demo.url('')
def index(req):
    return "This is a demo!"

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('0.0.0.0', 5678, demo)
    srv.serve_forever()
