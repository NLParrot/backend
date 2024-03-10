from chatapp.db.vec_db import VecDB
from chatapp.db.department_db import DepartmentDB
from chatapp.responses.select_response import SelectResponse


def _donot_understand():
    return SelectResponse().get_response("general/cannot_understand")


def _has_department_name(department_name):
    department_db = DepartmentDB()

    id = department_db.find_id_by_department(department_name)
    locations = department_db.find_all_location(id)
    contacts = department_db.find_all_contacts(id)

    # flatten out
    locations = [x[0] for x in locations]
    print(locations)
    print(contacts)

    response = (
        SelectResponse().get_response(
            "service/contacts_normal", {"department_name": department_name}
        )
        + "\n"
    )

    # generate information response
    response += "위치: "
    response += ", ".join(locations) + "\n"
    response += "연락처:\n"
    for contact_type, contact_value in contacts:
        response += f"  - {contact_type}: {contact_value}\n"

    return response


def contacts_response(slot):
    client = VecDB()

    department_name = client.query_department_name(slot.get("keyword"))
    if department_name == None:
        return _donot_understand()
    else:
        return _has_department_name(department_name)
