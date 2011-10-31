from stirling.daemons import Mongo

camp_clones = Mongo.search_clones('stirling.occupy.camp.Camp')
if camp_clones:
    Camp = camp_clones[0]
else:
    Camp = Mongo.clone_entity('stirling.occupy.camp.Camp')

