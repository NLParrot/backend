# type:ignore
import json
import logging
import pandas as pd
import tomllib
import random

from functools import wraps
from chatapp.db.course_db import CourseDB
from config import config

from .db.vec_db import VecDB
from .db.map_db import MapDB
from .intent_models import Intent2

from .actions.course.course_evaluation import course_evaluation_response


handlers = {
    Intent2.COURSE_EVALUATION: course_evaluation_response,
    Intent2.COURSE_INFORMATION: course_information_response,
}


class ChatResponse:
    def __init__(self):
        with open("./data/raw/department_data.json") as f:
            department_json = json.load(f)

        self.address_location_dict = {x["부서명"]: x for x in department_json}
        self.map = MapDB()

    def __call__(self, intent2, slot):
        for handler_intent2, func in handlers.items():
            if handler_intent2 == intent2:
                return func(slot)

        return "no response made yet"
        if a:
            pass
        elif intent2 == Intent2.BUILDING_LOCATION:
            return self.get_response_location(slot)
        elif intent2 == Intent2.PATHFIND:
            return self.get_response_pathfind(slot)
        elif intent2 == Intent2.CONTACTS:
            return self.get_response_contacts(slot)
        elif intent2 == Intent2.FA_INFORMATION:
            return self.get_response_fa_information(slot)
        elif intent2 == Intent2.RETAKE_INFORMATION:
            return self.get_response_retake_information(slot)

        return "no response made yet"

    # Need map information
    def get_response_location(self, slot):
        client = VecDB()

        location_name, coordinate = client.query_location_name(slot.get("location"))
        if location_name == None:
            return "이해하지 못했습니다! 다시 말해주세요!\n"

        response = f"{location_name}의 위치를 보여드릴게요\n"
        slot["location_name"] = location_name
        slot["coordinate"] = coordinate
        slot["display_location_map"] = True

        return response

    # Need map information
    def get_response_pathfind(self, slot):
        client = VecDB()

        from_loc_name, from_coord = client.query_location_name(
            slot.get("location_from")
        )
        to_loc_name, to_coord = client.query_location_name(slot.get("location_to"))
        logging.debug(f"from_coord={from_coord}")
        logging.debug(f"to_coord={to_coord}")

        if from_loc_name == None and to_loc_name == None:
            return "이해하지 못했습니다! 다시 말해주세요!\n"
        elif from_loc_name == None:
            slot["info_key"] = "location_from"
            slot["status"] = "need_info"
            return f"어디서부터 {to_loc_name}까지 가고 싶은지 이해하지 못했습니다! 다시 말해주세요\n"
        elif to_loc_name == None:
            slot["info_key"] = "location_to"
            slot["status"] = "need_info"
            return f"{from_loc_name}에서 어디로 가고 싶은지 이해하지 못했습니다! 다시 말해주세요!\n"

        start = self.map.closest_node(from_coord["latitude"], from_coord["longitude"])
        goal = self.map.closest_node(to_coord["latitude"], to_coord["longitude"])

        path = self.map.astar_multidigraph(start, goal)
        slot["path"] = path
        slot["display_path_map"] = True
        slot["location_from"] = from_loc_name
        slot["location_to"] = to_loc_name

        response = f"{from_loc_name}에서 {to_loc_name}까지 가는 길을 알려 드리겠습니다!\n"
        return response

    def get_response_contacts(self, slot):
        client = VecDB()

        department_name = client.query_department_name(slot.get("keyword"))
        if department_name == None:
            return "이해하지 못했습니다! 다시 말해주세요!\n"

        contacts = self.address_location_dict[department_name]

        response = f"{department_name}의 연락처를 찾으시나요? 제가 알려드릴게요!\n"

        for k, v in contacts.items():
            response += f"{k}: "
            if isinstance(v, dict):
                response += "\n"
                for kk, vv in v.items():
                    if isinstance(vv, list):
                        for l in vv:
                            response += f"  - {l}\n"
                    else:
                        response += f"- {kk} : {vv}\n"
            else:
                response += v + "\n"

        return response

    def get_response_fa_information(self, slot):
        response = "FA 관련은 학칙을 확인하는게 가장 정확합니다!\n"
        response += "관련 부분은 다음과 같습니다.\n\n"
        response += """제25조 (FA제도) ① 한 학기 동안 학생이 수강하는 과목에 대하여 결석허용 한계를 정하고 이를 초과할 경우에는 그 과목의 성적은 FA로 기록되며 과목낙제가 된다.
       ② 매 과목당 결석 허용 회수는 한 학기를 통산하여 주당 수업시간수의 두 배까지이다. 즉, 한 학기에 주당 3시간 과목은 6시간, 주당 2시간 과목은 4시간까지 결석이 허용된다. 3회의 지각은 한 번의 결석으로 환산된다. 
       ③ 졸업하는 마지막 학기의 결석 허용한계는 위 한계의 두 배이다. (여기서 졸업하는 학기란 졸업예정자로 확정된 학기를 말한다.)
       ④ 학생의 결석회수가 위의 허용한계에 도달될 경우, 이를 인터넷을 통하여 개별적으로 공고하여 해당 학생에게 경고한다. 모든 학생은 자신의 과목별 결석 및 지각회수를 기록 보관하여 FA경고에 항시 유의하여야 한다.<개정 2012.2.22>
       ⑤ 위의 결석허용 한계를 초과한 학생은 이를 공고하며, 해당과목의 성적은 과목낙제인 FA로 표시된다.<개정 2022.6.14>
       ⑥ 강의와 실험실습으로 구성된 과목에 있어서는 출결점검을 구분하여 처리하며 강의와 실험실습 중 어느 하나에서 FA를 받을 경우 그 과목 전체 성적이 FA가 된다.
       ⑦ 졸업예정 학기에 조기 취업 및 입사시험으로 인하여 부득이 제③항의 결석 허용한계 초과 시, 학생이 취업확인서(지정 서식)를 해당 기업(또는 기관)의 확인을 받아 학사지원팀에 제출할 경우, 담당교수 재량에 의하여 해당 근무기간을 출석으로 대체 인정할 수 있다. <신설 2016.10.14>
       ⑧ 제⑦항의 경우, 담당교수는 해당 교육과정 이수를 인정할만한 수업 과제나 시험을 통하여 평가를 하고, 이에 상응하는 성적을 부여하여야 한다. 다만, 이 경우 성적은 B+ 이하로 부여함을 원칙으로 한다. <신설 2016.10.14>

제26조 (유고결석) ① 다음 각 호의 사유에 의하여 결석하게 될 경우 사고발생전이나 발생 즉시 또는 부득이한 경우 발생일로부터 7일 이내에 증빙서류를 첨부하여 제1전공 소속 대학행정팀에 유고결석계를 제출하면 각 사유별 결석허용기간에 대해서는 결석으로 간주하지 않는다.<개정 2007.2.6., 2022.03.23>
        1. 부모 및 형제자매 사망, 본인 결혼시 7일(휴일 포함), 조부모 사망시 3일(장례일정이 3일 초과시 장례일까지/휴일 포함) <개정 2013.7.11, 2016.12.23>
        2. 입원치료, 전염성 질환 등 의사 소견상 등교가 불가능한 질병 또는 상해 치료의 경우 2주 이내 <개정 2013.7.11, 2016.12.23>
        3. 징병검사 등 병역관계 및 예비군훈련의 경우 통지서에 명기된 일수 <개정 2016.12.23>
        4. 학교현장실습 및 각 학과 학술여행, 야외실습, 기타 본교 주관 교육프로그램 참가의 경우 해당기간
        5. <삭제 2016.12.23>
        6. 정부기관의 요청에 의한 특별회합의 경우 해당시간
        7. 학생활동부서 임원의 국제회합 및 이에 준하는 경우 해당시간
        8. 신문 발간을 위한 정·부편집장의 긴급작업의 경우 해당시간
        9. 학교의 요청에 따른 교내·외 중요행사 참여의 경우 해당기간
  10. 긴급한 재난 재해, 1급 법정 감염병 및 기타 감염병 감염 또는 감염 의심 등 총장이 지정한 사유의 경우 해당 기간 <신설 2022.6.14.>
  11. 본인 출산시 20일, 배우자의 출산시 10일(출산일을 포함하여 출산전후로 신청 가능) <신설 2023.05.11>

       ② 다만, 제7호 및 제8호는 학생문화처장의 사전 승인을 얻은 경우에 한하여 제출할 수 있으며, 제9호는 총장의 승인을 받은 경우에 한하여 허용한다. <개정 2016.12.23>
       ③ 다음 각 호의 1에 해당하는 경우에는 유고결석으로 인정될 수 없다. 
        1. 신문기자의 신문발간 작업
        2. 각 동아리의 연습 및 공연
        3. 타교와의 운동 시합
        4. 교통편의 연착
        5. <삭제 2013.7.11>
        6. 가족의 병고
        7. 가사 및 개인사정
       [전문개정 2006.2.14]"""
        response += "\n\n출처: https://www.sogang.ac.kr/gopage/goboard12.jsp?bbsConfigFK=170&pkid=500062"
        return response

    def get_response_retake_information(self, slot):
        response = "재수강 제도에 대해서는 학칙을 확인하는게 가장 정확합니다.\n"
        response += "관련 부분은 다음과 같습니다.\n"
        response += """제15조 (재이수) ① 이미 이수한 교과목을 재이수할 수 있다. 재이수의 경우 전(前) 성적의 학적부 기록은 R(Re-registered)로 대체되며 새로이 취득한 성적으로 총성적평점평균(CGPA)을 계산한다.
       ② 재이수하여 취득한 성적은 “A⁻ ”를 초과할 수 없다. <개정 2006.2.14., 2014.12.11>
       ③ 재이수 과목은 본 시행세칙 제12조 ⑤항에 따른 수강신청 가능학점에 포함된다.<개정 2009.5.26., 2020.06.08>
       ④ 지도교수 및 학과장(전공주임교수)은 수강신청학점의 제한을 둘 수도 있다.<개정 2006.2.14>
       ⑤ 과목번호, 과목명 및 과목내용이 반드시 동일하여야 한다. 다만, 8학기 이상 재학생에 한하여 재이수할 과목이 당해 학기를 포함하여 재학한 직전 4학기 이내에 개설되지 않은 경우, 재이수 대상과목을 개설하는 전공 학과장의 요청으로 당해 학기에 개설된 타 과목으로 재이수 할 수 있다.<개정 2020.12.15.>
       ⑥ 이미 취득한 과목과 과목번호, 과목명이 동일한 과목은 신규수강과목으로 학점을 취득할 수 없다.
       ⑦ 재이수는 재학 중 8회 이내로 제한한다. 다만 계절수업 중 재이수는 재학 중 8회에 산입하지 않는다.<신설 2006.2.14, 개정 2014.12.11, 2020.06.08>
       ⑧ <신설 2007.2.6.><삭제 2023.09.06>
       ⑨ <삭제 2020.06.08>
       ⑩ 이미 이수한 교과목 중 ‘S(Successful)’ 등급을 받은 과목은 재이수할 수 없다.<2015.10.29>
       ⑪ 편입생이 전적대학에서 이수한 과목 중 본교 교과목으로 인정받은 과목은 재이수할 수 없다.<2015.10.29>"""
        response += "\n\n출처: https://www.sogang.ac.kr/gopage/goboard12.jsp?bbsConfigFK=170&pkid=500062"
        return response
