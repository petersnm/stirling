def toy_app(req):
    return 'It works. Sort of. WIP. HERP~'

from stirling.daemons.servers.http.middleware import StirlingWare

app = StirlingWare(toy_app)
