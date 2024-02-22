# type:ignore
import json
import logging
import pandas as pd

from chat_db import ChatDB
from intent_models import Intent2
from map import MapDB

logging.basicConfig(level=logging.DEBUG)


class ChatResponse:
    def __init__(self):
        with open("../data/address_data.json") as f:
            address_location_json = json.load(f)
        
        self.course = pd.read_csv("../data/course.csv") 
        
        self.address_location_dict = {x["부서명"]: x for x in address_location_json}
        self.map = MapDB()

    def __call__(self, intent2, slot):
        if intent2 == Intent2.COURSE_EVALUATION:
            return self.get_response_course_evaluation(slot)
        elif intent2 == Intent2.COURSE_INFORMATION:
            return self.get_response_course_info(slot)
        elif intent2 == Intent2.BUILDING_LOCATION:
            return self.get_response_location(slot)
        elif intent2 == Intent2.PATHFIND:
            return self.get_response_pathfind(slot)
        elif intent2 == Intent2.CONTACTS:
            return self.get_response_contacts(slot)

        return "no response made yet"

    def get_response_course_evaluation(self, slot):
        client = ChatDB()

        course = client.query_course(slot.get("course"))
        professor = client.query_professor(slot.get("professor"))

        if slot.get("course_keyword"):
            evaluations = client.query_evaluations(slot.get("course_keyword"))
        else:
            evaluations = client.query_evaluations("학점")

        response = f"{professor} 교수님의 {course} 강의에 대한 강의 평가를 찾으시는군요!\n"
        response += "몇가지를 보여드릴게요\n"
        response += f"1: {evaluations}"

        return response

    # Where to get Data?
    def get_response_course_info(self, slot):
        client = ChatDB()
        course = client.query_course(slot.get('course'))
        professor = client.query_professor(slot.get('professor'))
        

        if course == None and professor == None:
            return "교수님과 수업 이름을 제대로 인식하지 못했습니다. 다시 말해주세요!"

        # query about course + professor
        elif course and professor:
            res = [self.course.loc[self.course['교수진'] == professor & self.course['과목명'] == course]]
            response = f"{professor} 교수님의 {course} 수업에 대한 정보를 보여드리겠습니다!\n"

        # query all about course
        elif course:
            res = self.course.loc[self.course['교수진'] == professor]
            response = f"{course} 수업에 대한 정보를 보여드리겠습니다!\n"
        
        # query all about professor
        else:
            res = self.course.loc[self.course['과목명'] == course]
            response = f"{professor} 교수님이 여시는  수업에 대한 정보를 보여드리겠습니다!\n"

        #res.apply(lambda x: response += f"{res['과목명']}({res['과목번호']}, {res['교수진']})\n", axis=1)

        for r in res.iterrows():
            response += f"{r['과목명']}({r['과목번호']}) ({r['교수진']})\n"
            response += f"학점: {r['학점']}"
            response += f"수업시간: {r['수업시간/강의실']}\n"
            response += f"권장학년: {r['권장학년']}"

        return response

    # Need map information
    def get_response_location(self, slot):
        client = ChatDB()

        location_name, coordinate = client.query_location_name(slot["location"])

        response = f"{location_name}의 위치를 보여드릴게요\n"
        response += f"바로 여기!"
        slot["location_name"] = location_name
        slot["coordinate"] = coordinate
        slot["display_location_map"] = True

        return response

    # Need map information
    def get_response_pathfind(self, slot):
        client = ChatDB()

        from_loc_name, from_coord = client.query_location_name(slot["location_from"])
        to_loc_name, to_coord = client.query_location_name(slot["location_to"])
        logging.debug(f"from_coord={from_coord}")
        logging.debug(f"to_coord={to_coord}")
        start = self.map.closest_node(from_coord["latitude"], from_coord["longitude"])
        goal = self.map.closest_node(to_coord["latitude"], to_coord["longitude"])

        path = self.map.astar_multidigraph(start, goal)
        slot["path"] = path
        slot["display_path_map"] = True

        response = f"{from_loc_name}에서 {to_loc_name}까지 가는 길을 알려 드리겠습니다!\n"
        return response

    def get_response_contacts(self, slot):
        client = ChatDB()

        department_name = client.query_department_name(slot["keyword"])
        contacts = self.address_location_dict[department_name]

        response = f"{department_name}의 연락처를 찾으시나요? 제가 알려드릴게요!\n"
        response += f"{contacts}"

        return response
