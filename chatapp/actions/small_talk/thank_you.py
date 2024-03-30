
from chatapp.responses.select_response import SelectResponse


def thank_you_response(slot):
    return SelectResponse().get_response("small_talk/thank_you")
