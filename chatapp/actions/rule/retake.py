from chatapp.responses.select_response import SelectResponse


def retake_response(self, slot):
    return SelectResponse().get_response("rule/retake_normal")
    return response
