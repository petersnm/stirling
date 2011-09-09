import logging
logger = logging.getLogger(__name__)

from abzverse.webapps.rpg import rpg_app
from stirling.daemons.servers.http import app

app.dispatcher.add_rule('^/rpg/', rpg_app)
logger.info('abzverse running..')
