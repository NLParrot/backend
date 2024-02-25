# type:ignore
from transformers import (
    TextClassificationPipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
import logging


class Intent1:
    COURSE = "강의"
    MAP = "지도"
    SERVICE = "학교관련서비스"
    RULE = "학칙"

    def __init__(self, tokenizer_path, model_path):
        koelectra_tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path, local_fiels_only=True
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path, local_files_only=True
        )

        self.classifier = TextClassificationPipeline(
            model=self.model, tokenizer=koelectra_tokenizer
        )

    def __call__(self, user_text):
        intent1_s = self.classifier(user_text)[0]["label"]  # pyright: ignore
        intent1 = self._stoi1(intent1_s)

        return intent1

    def _stoi1(self, s):
        if s == "강의":
            return Intent1.COURSE
        elif s == "지도":
            return Intent1.MAP
        elif s == "학교괸련서비스":
            return Intent1.SERVICE
        elif s == "학칙":
            return Intent1.RULE
        else:
            raise ValueError(f"Intent1 not Valid: {s}")


class Intent2:
    COURSE_EVALUATION = "강의평가 요약"
    COURSE_INFORMATION = "특정 수업의 수업시간 및 장소"
    BUILDING_LOCATION = "건물 위치"
    PATHFIND = "길찾기"
    CONTACTS = "연락처"
    FA_INFORMATION = "FA제도"
    RETAKE_INFORMATION = "재수강"

    def __init__(self, tokenizer_path, course_path, map_path, service_path, rule_path):
        koelectra_tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path, local_fiels_only=True
        )

        self.course_model = AutoModelForSequenceClassification.from_pretrained(
            course_path, local_files_only=True
        )

        self.map_model = AutoModelForSequenceClassification.from_pretrained(
            map_path, local_files_only=True
        )

        self.service_model = AutoModelForSequenceClassification.from_pretrained(
            service_path, local_files_only=True
        )

        self.rule_model = AutoModelForSequenceClassification.from_pretrained(
            rule_path, local_files_only=True
        )

        self.course_classifier = TextClassificationPipeline(
            model=self.course_model, tokenizer=koelectra_tokenizer
        )

        self.map_classifier = TextClassificationPipeline(
            model=self.map_model, tokenizer=koelectra_tokenizer
        )

        self.service_classifier = TextClassificationPipeline(
            model=self.service_model, tokenizer=koelectra_tokenizer
        )

        self.rule_classifier = TextClassificationPipeline(
            model=self.rule_model, tokenizer=koelectra_tokenizer
        )

    def __call__(self, user_text, intent1):
        if intent1 == Intent1.COURSE:
            return self.get_intent2_course(user_text)
        elif intent1 == Intent1.MAP:
            return self.get_intent2_map(user_text)
        elif intent1 == Intent1.RULE:
            return self.get_intent2_school_rule(user_text)
        elif intent1 == Intent1.SERVICE:
            return self.get_intent2_school_service(user_text)
        else:
            raise ValueError("Intent1 Value Error in determining Intent2")

    def get_intent2_course(self, user_text):
        return self.course_classifier(user_text)[0]["label"]

    def get_intent2_map(self, user_text):
        return self.map_classifier(user_text)[0]["label"]

    def get_intent2_school_rule(self, user_text):
        return self.rule_classifier(user_text)[0]["label"]

    def get_intent2_school_service(self, user_text):
        return self.service_classifier(user_text)[0]["label"]
