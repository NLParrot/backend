

def test_get_response(select_response):
    res = select_response.get_response("map/building_location_normal", {"location_name": "asd"})
    assert res != "Error while selecting response"

def test_get_response_variable_not_satisfied(select_response):
    res = select_response.get_response("map/building_location_normal")
    assert res == "Error while selecting response"
    

