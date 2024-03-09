from chatapp.db.vec_db import VecDB
from chatapp.responses.select_response import SelectResponse


# Can't find matching course and professor name
def _course_none_professor_none():
    s = SelectResponse()
    return s.get_response("general/cannot_understand")


# Can't find matching course name
def _course_none(professor):
    s = SelectResponse()
    return s.get_response(
        "course/evaluations/only_know_professor", {"professor": professor}
    )


# Can't find matching professor name
def _professor_none(course):
    s = SelectResponse()
    return s.get_response("course/evaluations/only_know_course", {"course": course})


# Noone has evaluated this course before
def _evaluations_none(course, professor):
    s = SelectResponse()
    return s.get_response(
        "course/evaluations/no_evaluations", {"course": course, "professor": professor}
    )


# Course, professor matched, find evaluations on that course
def _all_available(client, course, professor, course_keyword):
    evaluations = client.query_evaluations(course, professor, course_keyword)

    if evaluations == None:
        return _evaluations_none(course, professor)

    # Get response from template
    response = (
        SelectResponse().get_response(
            "course/evaluations/evaluations_normal",
            {"course": course, "professor": professor},
        )
        + "\n"
    )

    # Dynamically add evaluations to response
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
