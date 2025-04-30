import psycopg2
from psycopg2.extras import RealDictCursor

from app.core.config import (DB_HOST,
                             DB_PASS,
                             DB_USER,
                             DB_NAME,
                             DB_SCHEMA)


class Database:
    def __init__(self):
        self.__conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        self.__conn.set_client_encoding('UTF8')
        self.__cursor = self.__conn.cursor()
        self.__check_on_schema()

    def __check_on_schema(self):
        if self.__cursor:
            self.__cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            if self.__cursor.fetchone()["count"] == 0:
                with open(DB_SCHEMA, 'r') as file:
                    sql_script = file.read()
                    self.__cursor.execute(sql_script)
            self.__conn.commit()

    def add_user(self, username, password, email):
        if self.__cursor:
            self.__cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING id",
                                  (username, password, email))
            self.__conn.commit()
            return self.__cursor.fetchone()["id"]
        return None

    def delete_user(self, user_id):
        if self.__cursor:
            self.__cursor.execute("DELETE FROM users WHERE id=%s",
                                  (user_id,))
            self.__conn.commit()
            return True
        return None

    def get_user_data(self, idx):
        if self.__cursor:
            self.__cursor.execute("SELECT * FROM users WHERE id=%s", (idx,))
            user_data = self.__cursor.fetchone()
            return user_data
        return None

    def get_user_id(self, username):
        if self.__cursor:
            self.__cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
            user_data = self.__cursor.fetchone()
            if user_data:
                return user_data["id"]
        return None

    def add_job(self, status, img, user_id):
        if self.__cursor:
            self.__cursor.execute("INSERT INTO deconvolution_jobs (status, img, user_id) VALUES (%s, %s, %s)",
                                  (status, img, user_id))
            self.__conn.commit()
            return self.__cursor.fetchone()[0]
        return None

    def update_job_status(self, idx, status):
        if self.__cursor:
            self.__cursor.execute("UPDATE deconvolution_jobs SET status = %s WHERE id = %s",
                                  (status, idx))
            self.__conn.commit()
            return True
        return False

    def add_result(self, job_id, img):
        if self.__cursor:
            self.__cursor.execute("INSERT INTO results (job_id, img) VALUES (%s, %s)",
                                  (job_id, img))
            self.__conn.commit()
            return self.__cursor.fetchone()[0]
        return None

    def change_user_username(self, user_id, username):
        if self.__cursor:
            self.__cursor.execute("UPDATE users SET username = %s WHERE id = %s",
                                  (username, user_id))
            self.__conn.commit()
            return True
        return False

    def change_user_password(self, user_id, password):
        if self.__cursor:
            self.__cursor.execute("UPDATE users SET password = %s WHERE id = %s",
                                  (password, user_id))
            self.__conn.commit()
            return True
        return False

    def close_connection(self):
        self.__cursor.close()
        self.__conn.close()
