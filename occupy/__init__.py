import logging

from stirling.daemons import Mongo


camp_clones = Mongo.search_clones('stirling.occupy.camp.Camp')
if camp_clones:
    logging.debug('found camp clone')
    Camp = camp_clones[0]
else:
    logging.debug('making new camp clone')
    Camp = Mongo.clone_entity('stirling.occupy.camp.Camp')

