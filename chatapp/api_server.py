from flask import Blueprint
from flask import request
import logging

from chatapp.intent_models import *
from chatapp.state_models import *
from chatapp.response import *

chat_blueprint = Blueprint("chatapp", __name__)

intent1 = Intent1()
intent2 = Intent2()
response = ChatResponse()
state = NERState()

log = logging.getLogger(__name__)
user_logger = logging.getLogger("user_logger")
user_logger_file_handler = logging.FileHandler("./log/dialogue.log", mode="a")
user_logger.setLevel(logging.INFO)
user_logger.addHandler(user_logger_file_handler)
user_logger.propagate = False


@chat_blueprint.route("/api/chat/message", methods=["POST"])
def chat():
    request_json = request.get_json()

    user_text = request_json.get("user_text", "")
    cur_intent1 = request_json.get("intent1")
    cur_intent2 = request_json.get("intent2")
    cur_slot = request_json

    cur_intent1 = intent1(user_text)
    cur_intent2 = intent2(user_text, cur_intent1)
    add_slot = state(user_text, cur_intent1, cur_intent2)
    cur_slot = cur_slot | add_slot

    response_text = response(cur_intent2, cur_slot)

    cur_slot["intent1"] = cur_intent1
    cur_slot["intent2"] = cur_intent2
    cur_slot["response_text"] = response_text

    log_dialogue(user_text, cur_intent1, cur_intent2, cur_slot, response_text)

    return cur_slot


def log_dialogue(user_text, intent1, intent2, slot, response_text):
    user_logger.info(f"u___%s___u", user_text)
    user_logger.info(f"i1___%s___1i", intent1)
    user_logger.info(f"i2___%s___2i", intent2)
    user_logger.info(f"s___%s___s", slot)
    user_logger.info(f"r___%s___r", response_text)
