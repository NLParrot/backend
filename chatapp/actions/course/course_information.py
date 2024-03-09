from chatapp.db.course_db import CourseDB
from chatapp.db.vec_db import VecDB
from chatapp.responses.select_response import SelectResponse


def _course_none_professor_none():
    return SelectResponse().get_response("general/cannot_understand")


def _course_not_opened_this_semester(course=None, professor=None):
    s = SelectResponse()
    if course == None:
        return s.get_response(
            "course/information/no_course_this_semester", {"course": course}
        )
    elif professor == None:
        return s.get_response(
            "course/information/no_professor_this_semester", {"professor": professor}
        )
    else:
        return s.get_response(
            "course/information/not_opened_this_semester",
            {"course": course, "professor": professor},
        )


def _response_course_info(row_list):
    response = ""
    for i, r in enumerate(row_list, 1):
        (
            id,
            major,
            course_code,
            division,
            course_name,
            credit,
            time,
            location,
            professor,
            is_english,
            target_year,
            recommended_year,
        ) = r

        response += f"{i}.\n"
        response += f"{course_name}({course_code}) ({professor})\n"
        response += f"학점: {credit}\n"
        response += f"수업시간: {time}\n"
        response += f"강의실: {location}\n"
        response += f"권장학년: {recommended_year}\n"

    return response


def _course_all(course):
    s = SelectResponse()
    course_db = CourseDB()
    res = course_db.find_by_course(course)
    if res == None:
        return _course_not_opened_this_semester(course=course)

    response = s.get_response("course/information/all_by_course", {"course": course})
    response += _response_course_info(res)

    return response


def _professor_all(professor):
    s = SelectResponse()
    course_db = CourseDB()
    res = course_db.find_by_professor(professor)
    if res == None:
        return _course_not_opened_this_semester(professor=professor)

    response = s.get_response(
        "course/information/all_by_professor", {"professor": professor}
    )
    response += _response_course_info(res)

    return response


def _course_and_professor(course, professor):
    course_db = CourseDB()
    res = course_db.find_by_course_and_professor(course, professor)
    if res == None:
        return _course_not_opened_this_semester(course, professor)

    response = (
        SelectResponse().get_response(
            "course/information/information_normal",
            {"course": course, "professor": professor},
        )
        + "\n"
    )
    response += _response_course_info(res)

    return response


def course_information_response(slot):
    client = VecDB()
    course, professor = client.query_course_professor(
        slot.get("course"), slot.get("professor")
    )

    # query about course + professor
    if course and professor:
        return _course_and_professor(course, professor)
    # query all about course
    elif course:
        return _course_all(course)
    # query all about professor
    elif professor:
        return _professor_all(professor)
    # Nothing known
    else:
        return _course_none_professor_none()
