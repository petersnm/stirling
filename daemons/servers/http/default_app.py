from stirling.daemons.servers.http.middleware import App

default = App('default')

@default.url('^/$')
def index(req):
    return "It works!"

@default.url('^/fbgm/$')
def fbgm(req):
    return "Fuck bitches, get money."
