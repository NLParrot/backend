
from chatapp.responses.select_response import SelectResponse


def bored_response():
    return SelectResponse().get_response("smalltalk/bored")
