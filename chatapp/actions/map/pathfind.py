from chatapp.db.map_db import MapDB
from chatapp.db.vec_db import VecDB
from chatapp.responses.select_response import SelectResponse

def _from_none_to_none():
    return SelectResponse().get_response("general/cannot_understand")

def _only_know_to(location_to):
    return SelectResponse().get_response("map/only_know_to", {
        "location_to": location_to
    })

def _only_know_from(location_from):
    return SelectResponse().get_response("map/only_know_from", {
        "location_from": location_from
    })

# Finds shortes path, returns response
def _find_path(slot, location_from, from_coord, location_to, to_coord):
    map = MapDB()
    start = map.closest_node(from_coord["latitude"], from_coord["longitude"])
    goal = map.closest_node(to_coord["latitude"], to_coord["longitude"])

    path = map.astar_multidigraph(start, goal)
    slot["path"] = path
    slot["display_path_map"] = True
    slot["location_from"] = location_from
    slot["location_to"] = location_to

    return SelectResponse().get_response("map/pathfind_normal", {
        "location_to": location_to,
        "location_from": location_from
    })

def get_response_pathfind(self, slot):
    client = VecDB()

    from_loc_name, from_coord = client.query_location_name(slot.get("location_from"))
    to_loc_name, to_coord = client.query_location_name(slot.get("location_to"))

    if from_loc_name == None and to_loc_name == None:
        return _from_none_to_none()
    # only exists to_location
    elif from_loc_name == None:
        slot["info_key"] = "location_from"
        slot["status"] = "need_info"
        return _only_know_to(to_loc_name)
    # only exists from_location
    elif to_loc_name == None:
        slot["info_key"] = "location_to"
        slot["status"] = "need_info"
        return _only_know_from(from_loc_name)
    else:
        return _find_path(slot, from_loc_name, from_coord, to_loc_name, to_coord)
