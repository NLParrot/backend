# type:ignore
import logging

from .intent_models import Intent2

from .actions.course.course_evaluation import course_evaluation_response
from .actions.course.course_information import course_information_response
from .actions.map.building_location import building_location_response
from .actions.map.pathfind import pathfind_response
from .actions.service.contacts import contacts_response
from .actions.rule.fa import fa_response
from .actions.rule.retake import retake_response


handlers = {
    Intent2.COURSE_EVALUATION: course_evaluation_response,
    Intent2.COURSE_INFORMATION: course_information_response,
    Intent2.BUILDING_LOCATION: building_location_response,
    Intent2.PATHFIND: pathfind_response,
    Intent2.CONTACTS: contacts_response,
    Intent2.FA_INFORMATION: fa_response,
    Intent2.RETAKE_INFORMATION: retake_response,
}


class ChatResponse:
    def __call__(self, intent2, slot):
        try:
            for handler_intent2, func in handlers.items():
                if handler_intent2 == intent2:
                    return func(slot)

            return "no response made yet"
        except e:
            logging.error(e)
            return "Error in handling chat response"
