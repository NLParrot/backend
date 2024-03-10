import sqlite3
from config import config


class DepartmentDB:
    def __init__(self):
        self.connection = sqlite3.connect(config.get_db_path("department"))

    def __del__(self):
        self.connection.close()

    def find_id_by_department(self, name):
        cursor = self.connection.cursor()

        return cursor.execute(
            """
            SELECT id
            FROM department 
            WHERE department_name=?;
            """,
            (name,),
        ).fetchone()[0]

    def find_all_location(self, id):
        cursor = self.connection.cursor()

        return cursor.execute(
            """
            SELECT DISTINCT location_name 
            FROM department NATURAL JOIN location
            WHERE id=?
            """,
            (id,),
        ).fetchall()

    def find_all_contacts(self, id):
        cursor = self.connection.cursor()

        return cursor.execute(
            """
            SELECT contact_type, contact_value
            FROM department NATURAL JOIN contacts
            WHERE id=?
            """,
            (id,),
        ).fetchall()
