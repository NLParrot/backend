import sqlite3
import json
import pandas as pd
import re


# Should execute this after deleting .db files


def insert_department_data():
    con = sqlite3.connect("./data/department.db")
    with con:
        cursor = con.cursor()
        # ddl
        with open("./data/schema/ddl_department.sql", "r") as f:
            ddl_sql = f.read()
        cursor.executescript(ddl_sql)

        # insert data
        with open("./data/raw/department_data.json") as f:
            department = json.load(f)
        for d in department:
            cursor.execute(
                "INSERT INTO department(department_name) values (?)", (d["부서명"],)
            )

            pk = cursor.lastrowid
            if isinstance(d.get("위치", []), list):
                for location in d.get("위치", []):
                    cursor.execute(
                        "INSERT INTO location(id, location_name) values (?, ?)",
                        (
                            pk,
                            location,
                        ),
                    )
            else:
                cursor.execute(
                    "INSERT INTO location(id, location_name) values (?, ?)",
                    (
                        pk,
                        d["위치"],
                    ),
                )

            for k, v in d["연락처"].items():
                if isinstance(v, list):
                    for vv in v:
                        cursor.execute(
                            "INSERT INTO contacts(id, contact_type, contact_value) values (?, ?, ?)",
                            (pk, k, vv),
                        )

                else:
                    cursor.execute(
                        "INSERT INTO contacts(id, contact_type, contact_value) values (?, ?, ?)",
                        (pk, k, v),
                    )
    con.close()


def insert_building_data():
    con = sqlite3.connect("./data/building.db")
    with con:
        cursor = con.cursor()
        # ddl
        with open("./data/schema/ddl_building.sql", "r") as f:
            ddl_sql = f.read()
        cursor.executescript(ddl_sql)

        with open("./data/raw/building_data.json", "r") as f:
            building_json = json.load(f)

        for building in building_json:
            loc = building["위치"]
            cursor.execute(
                "INSERT INTO building (latitude, longitude) values (?, ?)",
                (loc["위도"], loc["경도"]),
            )
            pk = cursor.lastrowid

            for n in building["건물명"]:
                cursor.execute(
                    "INSERT INTO building_names (id, building_name) values (?, ?)",
                    (pk, n),
                )
    con.close()


def insert_course_data():
    con = sqlite3.connect("./data/course.db")
    with con:
        cursor = con.cursor()
        # ddl
        with open("./data/schema/ddl_course.sql", "r") as f:
            ddl_sql = f.read()
        cursor.executescript(ddl_sql)

        course = pd.read_csv("./data/raw/course.csv")
        for _, r in course.iterrows():
            if pd.notnull(r["수업시간/강의실"]):
                mt = re.match(r"^(.+)\[(.+)\]$", r["수업시간/강의실"])
                if mt == None:
                    time = r["수업시간/강의실"]
                    location = ""
                else:
                    time = mt[1]
                    location = mt[2]

            else:
                time, location = "", ""

            if pd.notnull(r["영어강의"]):
                is_english = False
            else:
                is_english = True

            cursor.execute(
                "INSERT INTO course (major, course_code, division, course_name, credit, time, location, professor, is_english, target_year, recommended_year) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    r["학과"],
                    r["과목번호"],
                    r["분반"],
                    r["과목명"],
                    r["학점"],
                    time,
                    location,
                    r["교수진"],
                    is_english,
                    r["수강대상"],
                    r["권장학년"],
                ),
            )
    con.close()


if __name__ == "__main__":
    insert_department_data()
    insert_building_data()
    insert_course_data()
