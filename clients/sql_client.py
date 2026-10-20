import sqlite3
from configs.settings import DATABASE_PATH
from pathlib import Path


class SQLClient:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = database_path

    def execute_query(self, sql):
        # verify database file exists
        database_file = Path(self.database_path)
        if not self.database_path:
            raise Exception(f"database path DATABAES_PATH is not set. please set in environment")
        if not database_file.exists():
            raise FileNotFoundError(f"database file provided not exist. DF file: {self.database_file}")

        # DATABASE_PATH = "/Users/schen/api-testing/QA-Automation/job-tracker-app-for-testing/backend/data/job_tracker.db"
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()  # data is list
        cursor.close()
        connection.close()
        return [dict(row) for row in data]