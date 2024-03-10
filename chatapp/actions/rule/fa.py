from chatapp.responses.select_response import SelectResponse

def fa_response(self, slot):
    return SelectResponse().get_response("rule/fa_normal")
