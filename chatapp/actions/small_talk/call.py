
from chatapp.responses.select_response import SelectResponse


def call_response(slot):
    return SelectResponse().get_response("small_talk/call")
