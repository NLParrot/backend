from abc import abstractmethod
import torch
import logging
import re
from intent_models import Intent1, Intent2
from transformers import AutoModelForSeq2SeqLM, AutoModelForTokenClassification, AutoTokenizer
from transformers import TokenClassificationPipeline

logging.basicConfig(level=logging.DEBUG)

class StateModels:
    @abstractmethod
    def get_slot(self, user_text, intent1, intent2) -> dict:
        ...

class NERState(StateModels):
    def __init__(self, path):
        tokenizer = AutoTokenizer.from_pretrained(
            path, local_files_only=True
        )
        model = AutoModelForTokenClassification.from_pretrained(
            path, local_files_only=True
        )
        self.classifier = TokenClassificationPipeline(
            model=model, tokenizer=tokenizer, aggregation_strategy='first'
        )

    # underscored variables are not used in this State Model
    def __call__(self, user_text, _intent1, _intent2) -> dict:
        slot = {}
        classified = self.classifier(user_text)
        for group in classified:
            slot[group['entity_group']] = group['word']
        logging.debug(f"(state)slot={slot}")
        return slot

class Seq2SeqState(StateModels):
    def __init__(
        self, tokenizer_path, course_path, location_path, pathfind_path, service_path
    ):
        self.state_tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path, local_files_only=True
        )

        self.state_course_model = AutoModelForSeq2SeqLM.from_pretrained(
            course_path, local_files_only=True
        )

        self.state_location_model = AutoModelForSeq2SeqLM.from_pretrained(
            location_path, local_files_only=True
        )

        self.state_pathfind_model = AutoModelForSeq2SeqLM.from_pretrained(
            pathfind_path, local_files_only=True
        )

        self.state_service_model = AutoModelForSeq2SeqLM.from_pretrained(
            service_path, local_files_only=True
        )

        self.course_infer = Text2TextWithTokens(
            self.state_course_model, self.state_tokenizer
        )
        self.location_infer = Text2TextWithTokens(
            self.state_location_model, self.state_tokenizer
        )
        self.pathfind_infer = Text2TextWithTokens(
            self.state_pathfind_model, self.state_tokenizer
        )
        self.service_infer = Text2TextWithTokens(
            self.state_service_model, self.state_tokenizer
        )

    def __call__(self, user_text, intent1, intent2) -> dict:
        try:
            if intent1 == Intent1.COURSE:
                return self.get_slot_course(user_text)
            elif intent1 == Intent1.MAP:
                if intent2 == Intent2.BUILDING_LOCATION:
                    return self.get_slot_location(user_text)
                elif intent2 == Intent2.PATHFIND:
                    return self.get_slot_pathfind(user_text)
            elif intent1 == Intent1.RULE or intent1 == Intent1.SERVICE:
                return self.get_slot_service(user_text)
        except Exception as e:
            logging.error(e)

        return {}

    def get_slot_course(self, user_text) -> dict:
        inf = self.course_infer(user_text)
        logging.info(inf)
        output = re.sub(r"\[BOS\]", "", inf)
        output = re.sub(r"\[EOS\]", "", output)
        output = re.split(r"\[SEP\]", output)

        return {
            "course_keyword": output[1],
            "course": output[2],
            "professor": output[3],
        }

    def get_slot_location(self, user_text) -> dict:
        inf = self.location_infer(user_text)
        logging.info(inf)
        output = re.sub(r"\[BOS\]", "", inf)
        output = re.sub(r"\[EOS\]", "", output)
        output = re.split(r"\[SEP\]", output)
        return {"location": "k관"}

    def get_slot_pathfind(self, user_text) -> dict:
        inf = self.pathfind_infer(user_text)
        logging.info(inf)
        output = re.sub(r"\[BOS\]", "", inf)
        output = re.sub(r"\[EOS\]", "", output)
        output = re.split(r"\[SEP\]", output)
        return {"location_from": "로욜라", "location_to": "우정원"}

    def get_slot_service(self, user_text) -> dict:
        inf = self.service_infer(user_text)
        logging.info(inf)
        output = re.sub(r"\[BOS\]", "", inf)
        output = re.sub(r"\[EOS\]", "", output)
        output = re.split(r"\[SEP\]", output)
        return {"keyword": output[1]}


class Text2TextWithTokens:
    def __init__(self, model, tokenizer, gen_args={}, device=None):
        self.model = model
        self.tokenizer = tokenizer
        self.gen_args = gen_args
        if device == None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device

    def __call__(self, data):
        data = self.tokenizer(data, return_tensors="pt").to(self.device)
        model = self.model.to(self.device)
        output = model.generate(data["input_ids"], *self.gen_args)[0]
        return self.tokenizer.decode(output.tolist(), skip_special_tokens=False)
