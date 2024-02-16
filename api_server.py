from flask import Flask, request
from flask_cors import CORS

from transformers import TextClassificationPipeline
from transformers import AutoModelForSequenceClassification, AutoModelForSeq2SeqLM
from transformers import AutoTokenizer

import pandas as pd
import numpy as np
import logging
import torch
import re
import sys


# Logging
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
root_logger.addHandler(handler)

class Text2TextWithTokens:
    def __init__(self, model, tokenizer, gen_args={}, device=None):
        self.model = model
        self.tokenizer = tokenizer
        self.gen_args = gen_args
        if device == None:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.device = device
    def __call__(self, data):
        data = self.tokenizer(data, return_tensors='pt').to(self.device)
        model = self.model.to(self.device)
        output = model.generate(data['input_ids'], *self.gen_args)[0]
        return self.tokenizer.decode(output.tolist(), skip_special_tokens=False)

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

state_tokenizer = AutoTokenizer.from_pretrained(
    "./models/state_course_1", local_files_only=True
)

state_course_model = AutoModelForSeq2SeqLM.from_pretrained(
    "./models/state_course_1", local_files_only=True
)

state_location_model = AutoModelForSeq2SeqLM.from_pretrained(
    "./models/state_location_1", local_files_only=True
)

state_pathfind_model = AutoModelForSeq2SeqLM.from_pretrained(
    "./models/state_pathfind_1", local_files_only=True
)

state_service_model = AutoModelForSeq2SeqLM.from_pretrained(
    "./models/state_service_1", local_files_only=True
)

state_course_inference = Text2TextWithTokens(state_course_model, state_tokenizer)
state_location_inference = Text2TextWithTokens(state_location_model, state_tokenizer)
state_pathfind_inference = Text2TextWithTokens(state_pathfind_model, state_tokenizer)
state_service_inference = Text2TextWithTokens(state_service_model, state_tokenizer)

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
    add_slot = get_slot(intent1, intent2, user_text)
    slot = slot | add_slot

    response_text = get_response(intent1, intent2, slot)

    return {
        "intent1": intent1,
        "intent2": intent2,
        "slot": slot,
        "debug_text": f"intent1={intent1} intent2={intent2} slot={slot}",
        "response_text": response_text
        
    }

def get_response(intent1, intent2, slot):
    if intent2 == "강의평가 요약":
        return get_response_course_evaluation(slot)
    elif intent2 == "특정 수업의 수업시간 및 장소":
        return get_response_course_info(slot)
    elif intent2 == "건물 위치":
        return get_response_location(slot)
    elif intent2 == "길찾기":
        return get_response_pathfind(slot)
    elif intent2 == "연락처":
        pass
    elif intent2 == "학생복지":
        pass
    elif intent2 == "휴학":
        pass
    elif intent2 == "FA제도":
        pass
    elif intent2 == "재수강":
        pass


    return "no response made yet"

def get_response_course_evaluation(slot):
    pass

def get_response_course_info(slot):
    pass

def get_response_location(slot):
    pass

def get_response_pathfind(slot):
    pass


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


def get_slot(intent1, intent2, user_text):
    if intent1 == "강의":
        return get_slot_course(user_text)
    elif intent1 == "지도":
        if intent2 == "건물 위치":
            return get_slot_location(user_text)
        elif intent2 == "길찾기":
            return get_slot_pathfind(user_text)
    elif intent1 == "학칙" or intent1 == "학교관련서비스":
        return get_slot_service(user_text)

def get_slot_course(user_text):
    try:
        inf = state_course_inference(user_text)
        logging.info(inf)
        output = re.sub(r'\[BOS\]', '', inf)
        output = re.sub(r'\[EOS\]', '', output)
        output = re.split(r'\[SEP\]', output)

        return {
            'course_keyword': output[1],
            'course': output[2],
            'professor': output[3]
        }
    except Exception as e:
        logging.error(e)
        return {}

def get_slot_location(user_text):
    try:
        inf = state_location_inference(user_text)
        logging.info(inf)
        output = re.sub(r'\[BOS\]', '', inf)
        output = re.sub(r'\[EOS\]', '', output)
        output = re.split(r'\[SEP\]', output)
        return {
            'location': output[1]
        }
    except Exception as e:
        logging.error(e)
        return {}
    

def get_slot_pathfind(user_text):
    try:
        inf = state_pathfind_inference(user_text)
        logging.info(inf)
        output = re.sub(r'\[BOS\]', '', inf)
        output = re.sub(r'\[EOS\]', '', output)
        output = re.split(r'\[SEP\]', output)
        return {
            'location_from': output[1],
            'location_to': output[2]
        }
    except Exception as e:
        logging.error(e)
        return {}


def get_slot_service(user_text):
    try:
        inf = state_service_inference(user_text)
        logging.info(inf)
        output = re.sub(r'\[BOS\]', '', inf)
        output = re.sub(r'\[EOS\]', '', output)
        output = re.split(r'\[SEP\]', output)
        return {
            'keyword': output[1]
        }
    except Exception as e:
        logging.error(e)
        return {}

if __name__ == "__main__":
    app.run(port=5000)
