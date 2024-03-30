
from chatapp.responses.select_response import SelectResponse


def thank_you_response():
    return SelectResponse().get_response("smalltalk/thank_you")
