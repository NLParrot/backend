
from chatapp.responses.select_response import SelectResponse


def call_response():
    return SelectResponse().get_response("smalltalk/call")
