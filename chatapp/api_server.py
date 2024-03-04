
from flask import Flask
from flask import request
from flask_cors import CORS
import logging

from intent_models import *
from state_models import *
from response import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8000"}})

intent1 = Intent1(
    tokenizer_path="../models/intent1_model_1", model_path="../models/intent1_model_1"
)
intent2 = Intent2(
    tokenizer_path="../models/intent1_model_1",
    course_path="../models/intent2_course_model_1",
    map_path="../models/intent2_map_model_1",
    service_path="../models/intent2_school_service_model_1",
    rule_path="../models/intent2_school_rule_model_1",
)
response = ChatResponse()
state = NERState("../models/ner_1")

log = logging.getLogger(__name__)
user_logger = logging.getLogger("user_logger")
user_logger_file_handler = logging.FileHandler("../log/dialogue.log", mode="a")
user_logger.setLevel(logging.INFO)
user_logger.addHandler(user_logger_file_handler)
user_logger.propagate = False

@app.route("/api/chat/message", methods=["POST"])
def chat():
    request_json = request.get_json()
    log.debug(request_json)

    user_text = request_json.get("user_text", "")
    cur_intent1 = request_json.get("intent1")
    cur_intent2 = request_json.get("intent2")
    cur_slot = request_json

    if cur_slot["status"] != "need_info":
        cur_intent1 = intent1(user_text)
        cur_intent2 = intent2(user_text, cur_intent1)
        logging.debug(f"intent1={cur_intent1}")
        logging.debug(f"intent2={cur_intent2}")
        add_slot = state(user_text, cur_intent1, cur_intent2)
        cur_slot = cur_slot | add_slot
    else:
        cur_slot[cur_slot["info_key"]] = user_text
        cur_slot["status"] = "normal"

    response_text = response(cur_intent2, cur_slot)

    cur_slot["intent1"] = cur_intent1
    cur_slot["intent2"] = cur_intent2
    cur_slot["response_text"] = response_text

    user_logger.info(f"u___%s___u", user_text)
    user_logger.info(f"i1___%s___1i", cur_intent1)
    user_logger.info(f"i2___%s___2i", cur_intent2)
    user_logger.info(f"s___%s___s", cur_slot)
    user_logger.info(f"r___%s___r", response_text)
    return cur_slot



if __name__ == "__main__":
    app.run(port=5000)
