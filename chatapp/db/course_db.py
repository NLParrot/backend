import sqlite3
from config import config


class CourseDB:
    def __init__(self):
        self.connection = sqlite3.connect(config.get_db_path("course"))

    def __del__(self):
        self.connection.close()

    def find_by_course(self, course):
        cursor = self.connection.cursor()

        return cursor.execute(
            "SELECT * FROM course WHERE course_name=?", (course,)
        ).fetchall()

    def find_by_professor(self, professor):
        cursor = self.connection.cursor()

        return cursor.execute(
            "SELECT * FROM course WHERE professor=?", (professor,)
        ).fetchall()

    def find_by_course_and_professor(self, course, professor):
        cursor = self.connection.cursor()

        return cursor.execute(
            "SELECT * FROM course WHERE course_name=? AND professor=?",
            (course, professor),
        ).fetchall()
