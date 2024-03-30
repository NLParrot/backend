# type:ignore
from transformers import (
    TextClassificationPipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

from config import config


class Intent1:
    COURSE = "course"
    MAP = "map"
    SERVICE = "service"
    RULE = "rule"
    SMALL_TALK = "small_talk"

    def __init__(self):
        koelectra_tokenizer = AutoTokenizer.from_pretrained(
            config.get_model_path("intent1"), local_fiels_only=True
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.get_model_path("intent1"), local_files_only=True
        )

        self.classifier = TextClassificationPipeline(
            model=self.model, tokenizer=koelectra_tokenizer
        )

    def __call__(self, user_text):
        intent1 = self.classifier(user_text)[0]["label"]

        return intent1


class Intent2:
    # course
    COURSE_EVALUATION = "course_evaluation"
    COURSE_INFORMATION = "course_information"

    # map
    BUILDING_LOCATION = "building_location"
    PATHFIND = "pathfind"
    
    # service
    CONTACTS = "contacts"
    WELFARE = "welfare"
    CAMPUS_MEAL = "campus_meal"

    # rule
    FA_GENERAL = "fa_general"
    RETAKE = "retake"
    ACADEMIC_SCHEDULE = "academic_schedule"
    EXCHANGE_STUDENT = "exchange_student"
    SCHOLARSHIP = "scholarship"
    CURRICULUM = "curriculum"
    LEAVE_OF_ABSENCE = "leave_of_absence"
    TUITION_FEE = "tuition_fee"
    COURSE_REGISTRATION = "course_registration"

    # small_talk
    CALL = "call"
    BORED = "bored"
    THANK_YOU = "thank_you"
    HELP = "help"
    GREETING = "greeting"

    # misc
    MISC = "misc"

    def __init__(self):
        koelectra_tokenizer = AutoTokenizer.from_pretrained(
            config.get_model_path("intent1"), local_fiels_only=True
        )

        self.course_model = AutoModelForSequenceClassification.from_pretrained(
            config.get_model_path("intent2_course"), local_files_only=True
        )

        self.map_model = AutoModelForSequenceClassification.from_pretrained(
            config.get_model_path("intent2_map"), local_files_only=True
        )

        self.service_model = AutoModelForSequenceClassification.from_pretrained(
            config.get_model_path("intent2_service"), local_files_only=True
        )

        self.rule_model = AutoModelForSequenceClassification.from_pretrained(
            config.get_model_path("intent2_rule"), local_files_only=True
        )

        self.small_talk_model = AutoModelForSequenceClassification.from_pretrained(
            config.get_model_path("intent2_small_talk"), local_files_only=True
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

        self.small_talk_classifier = TextClassificationPipeline(
            model=self.small_talk_model, tokenizer=koelectra_tokenizer
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
        elif intent1 == Intent1.SMALL_TALK:
            return self.get_intent2_small_talk(user_text)
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
    
    def get_intent2_small_talk(self, user_text):
        return self.small_talk_classifier(user_text)[0]["label"]
