from stirling.daemons.servers.http.middleware import Dispatcher
from stirling.daemons.servers.http import app

#\rpg_app = app.new_ware('^/rpg/')
rpg_app = Dispatcher()

@rpg_app.bind('')
def index(req):
    return "RPG!"
