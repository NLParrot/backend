from chatapp.db.vec_db import VecDB
from chatapp.responses.select_response import SelectResponse


def building_location_response(slot):
    client = VecDB()
    s = SelectResponse()

    location_name, coordinate = client.query_location_name(slot.get("location"))
    if location_name == None:
        return s.get_response("general/cannot_understand")

    slot["location_name"] = location_name
    slot["coordinate"] = coordinate
    slot["display_location_map"] = True

    return s.get_response(
        "map/building_location_normal", {"location_name": location_name}
    )
