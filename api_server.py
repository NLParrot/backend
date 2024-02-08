from flask import Flask, request
from flask_cors import CORS

from transformers import TextClassificationPipeline
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

import pandas as pd
import numpy as np
import logging

# Logging
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO)

# Initialize some global variables
# Models that are used in pytorch

koelectra_tokenizer = AutoTokenizer.from_pretrained(
    "./models/intent1_model_1", local_fiels_only=True
)

intent1_model = AutoModelForSequenceClassification.from_pretrained(
    "./models/intent1_model_1", local_files_only=True
)

intent2_course_model = AutoModelForSequenceClassification.from_pretrained(
    "./models/intent2_course_model_1", local_files_only=True
)

intent2_map_model = AutoModelForSequenceClassification.from_pretrained(
    "./models/intent2_map_model_1", local_files_only=True
)

intent2_school_service_model = AutoModelForSequenceClassification.from_pretrained(
    "./models/intent2_school_service_model_1", local_files_only=True
)

intent2_school_rule_model = AutoModelForSequenceClassification.from_pretrained(
    "./models/intent2_school_rule_model_1", local_files_only=True
)

intent1_classifier = TextClassificationPipeline(
    model=intent1_model, tokenizer=koelectra_tokenizer
)

intent2_course_classifier = TextClassificationPipeline(
    model=intent2_course_model, tokenizer=koelectra_tokenizer
)

intent2_map_classifier = TextClassificationPipeline(
    model=intent2_map_model, tokenizer=koelectra_tokenizer
)

intent2_school_service_classifier = TextClassificationPipeline(
    model=intent2_school_service_model, tokenizer=koelectra_tokenizer
)

intent2_school_rule_classifier = TextClassificationPipeline(
    model=intent2_school_rule_model, tokenizer=koelectra_tokenizer
)

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {"origins": "http://127.0.0.1:8000"}
})



@app.route("/api/chat/message", methods=["POST"])
def get_state():
    request_json = request.get_json()
    logging.info(request_json)

    user_text = request_json["user_text"]
    slot = request_json.get("slot")
    intent1 = request_json.get("intent1")
    intent2 = request_json.get("intent2")

    intent1 = get_intent1(slot, user_text)
    intent2 = get_intent2(slot, user_text, intent1)


    return {
        "intent1": intent1,
        "intent2": intent2,
        "slot": slot,
        "response_text": f"intent1={intent1} intent2={intent2} slot={slot}"
    }


def get_intent1(slot, user_text):
    # slot: {context}, user_input: ""
    intent1 = intent1_classifier(user_text)[0]["label"]  # pyright: ignore
    logging.info(f"intent1={intent1}")

    return intent1

def get_intent2(slot, user_text, intent1):
    if intent1 == "강의":
        return get_intent2_course(user_text)
    elif intent1 == "지도":
        return get_intent2_map(user_text)
    elif intent1 == "학칙":
        return get_intent2_school_rule(user_text)
    elif intent1 == "학교관련서비스":
        return get_intent2_school_service(user_text)
    elif intent1 == "동아리":
        return get_intent2_school_club(user_text)
    return ""


def get_intent2_course(user_text):
    return intent2_course_classifier(user_text)[0]["label"] # pyright: ignore
    
def get_intent2_map(user_text):
    return intent2_map_classifier(user_text)[0]["label"] # pyright: ignore

def get_intent2_school_rule(user_text):
    return intent2_school_rule_classifier(user_text)[0]["label"] # pyright: ignore

def get_intent2_school_service(user_text):
    return intent2_service_classifier(user_text)[0]["label"] # pyright: ignore


# Not yet implemented
def get_intent2_school_club(user_text):
    return intent2_course_classifier(user_text)[0]["label"] # pyright: ignore


if __name__ == "__main__":
    app.run(port=5000)
