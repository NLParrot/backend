from chatapp.responses.select_response import SelectResponse


def greeting_response():
    return SelectResponse().get_response("smalltalk/greeting")
