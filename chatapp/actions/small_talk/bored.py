
from chatapp.responses.select_response import SelectResponse


def bored_response(slot):
    return SelectResponse().get_response("small_talk/bored")
