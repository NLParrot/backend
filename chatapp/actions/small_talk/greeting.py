from chatapp.responses.select_response import SelectResponse


def greeting_response(slot):
    return SelectResponse().get_response("small_talk/greeting")
