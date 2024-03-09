from chatapp.db.vec_db import VecDB
from chatapp.responses.select_response import SelectResponse

# Can't find matching course and professor name
def _course_none_professor_none():
    s = SelectResponse()
    return s.get_response("general/cannot_understand")

# Can't find matching course name
def _course_none(professor):
    return f"{professor} 교수님의 어떤 수업을 말하시는지 이해하지 못했습니다. 수업명을 다시 알려주세요\n"

# Can't find matching professor name
def _professor_none(course):
    return f"어떤 교수님의 {course} 수업을 말하시는지 이해하지 못했습니다. 교수님 이름을 다시 입력해주세요\n"

# Noone has evaluated this course before
def _evaluations_none(course, professor):
    return f"{professor} 교수님의 {course} 강의를 찾을 수 없습니다. 무슨 강의인지 찾지 못했습니다"

# Course, professor matched, find evaluations on that course
def _all_available(client, course, professor, course_keyword):
    evaluations = client.query_evaluations(
        course, professor, course_keyword
    )

    if evaluations == None:
        return _evaluations_none(course, professor)

    response = f"{professor} 교수님의 {course} 강의에 대한 강의 평가를 찾으시는군요!\n"
    response += "몇가지를 보여드릴게요\n"
    for i, eval in enumerate(evaluations, 1):
        response += f"# {i}\n{eval}\n\n"

    return response


def course_evaluation_response(slot):
    client = VecDB()

    course, professor = client.query_course_professor(
        slot.get("course"), slot.get("professor")
    )

    # Response changes based on combination of course, professor that are not None
    if course == None and professor == None:
        return _course_none_professor_none()
    elif course == None:
        return _course_none(professor)
    elif professor == None:
        return _professor_none(course)

    return _all_available(client, course, professor, slot.get("course_keyword"))



