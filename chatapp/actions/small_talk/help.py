
from chatapp.responses.select_response import SelectResponse


def help_response(slot):
    return SelectResponse().get_response("small_talk/help")
