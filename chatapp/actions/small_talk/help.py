
from chatapp.responses.select_response import SelectResponse


def help_response():
    return SelectResponse().get_response("smalltalk/help")
