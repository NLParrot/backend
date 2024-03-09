import sqlite3
from config import config


class DepartmentDB:
    def __init__(self):
        self.connection = sqlite3.connect(config.get_db_path("department"))

    def __del__(self):
        self.connection.close()

    def find_by_department(self, name):
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM")
