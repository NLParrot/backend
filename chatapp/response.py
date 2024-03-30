# type:ignore
import logging
from chatapp.actions.small_talk.bored import bored_response

from chatapp.actions.small_talk.call import call_response
from chatapp.actions.small_talk.greeting import greeting_response
from chatapp.actions.small_talk.help import help_response
from chatapp.actions.small_talk.thank_you import thank_you_response

from .intent_models import Intent2

from .actions.course.course_evaluation import course_evaluation_response
from .actions.course.course_information import course_information_response
from .actions.map.building_location import building_location_response
from .actions.map.pathfind import pathfind_response
from .actions.service.contacts import contacts_response
from .actions.rule.fa import fa_response
from .actions.rule.retake import retake_response


handlers = {
    # course
    Intent2.COURSE_EVALUATION: course_evaluation_response,
    Intent2.COURSE_INFORMATION: course_information_response,

    # map
    Intent2.BUILDING_LOCATION: building_location_response,
    Intent2.PATHFIND: pathfind_response,

    # service
    Intent2.CONTACTS: contacts_response,

    # rule
    Intent2.FA_GENERAL: fa_response,
    Intent2.RETAKE: retake_response,

    # small_talk
    Intent2.CALL: call_response,
    Intent2.GREETING: greeting_response,
    Intent2.HELP: help_response,
    Intent2.BORED: bored_response,
    Intent2.THANK_YOU: thank_you_response,
}


class ChatResponse:
    def __call__(self, intent2, slot):
        try:
            for handler_intent2, func in handlers.items():
                if handler_intent2 == intent2:
                    return func(slot)

            return "지금 하신 이야기에 대한 답변은 준비가 되지 않았습니다."
        except Exception as e:
            logging.error(e)
            return "Error in handling chat response"
