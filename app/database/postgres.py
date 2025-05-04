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
        """
        Функция, которая проверяет на наличие схемы таблиц в базе данных.
        Если нет, то создает их.

        :return: None.
        """

        if self.__cursor:
            self.__cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            if self.__cursor.fetchone()["count"] == 0:
                with open(DB_SCHEMA, 'r') as file:
                    sql_script = file.read()
                    self.__cursor.execute(sql_script)
            self.__conn.commit()

    def add_user(self, username, password, email):
        if self.__cursor:
            self.__cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING id",
                (username, password, email))
            self.__conn.commit()
            return self.__cursor.fetchone()["id"]
        return None

    def delete_user(self, user_id):
        """
        Функция для удаления пользователя из базы данных.

        Удаляет сначала все записи пользователя в таблице results,
        затем в deconvolution_jobs, потом самого пользователя.

        :param user_id: Идентификатор пользователя в БД
        :return: True или False
        """
        if self.__cursor:
            self.__cursor.execute("DELETE FROM results WHERE user_id=%s",
                                  (user_id,))
            self.__cursor.execute("DELETE FROM deconvolution_jobs WHERE user_id=%s",
                                  (user_id,))
            self.__cursor.execute("DELETE FROM users WHERE id=%s",
                                  (user_id,))
            self.__conn.commit()
            return True
        return False

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
            self.__cursor.execute("""
                INSERT INTO deconvolution_jobs (status, img, user_id) VALUES (%s, %s, %s) RETURNING id""",
                                  (status, img, user_id,))
            self.__conn.commit()
            return self.__cursor.fetchone()["id"]
        return None

    def update_job_status(self, idx, status):
        """
        Позволяет обновлять статус текущей задачи на деконволюцию.
        Например, при создании задачи устанавливается статус "В процессе",
        затем после выполнения "Завершено".

        :param idx: Идентификатор задачи в таблице deconvolution_jobs.
        :param status: Статус.
        :return: True или False.
        """

        if self.__cursor:
            self.__cursor.execute("UPDATE deconvolution_jobs SET status = %s WHERE id = %s",
                                  (status, idx))
            self.__conn.commit()
            return True
        return False

    def add_result(self, job_id, user_id, img):
        if self.__cursor:
            self.__cursor.execute("INSERT INTO results (job_id, user_id, img) VALUES (%s, %s, %s) RETURNING id",
                                  (job_id, user_id, img))
            self.__conn.commit()
            return self.__cursor.fetchone()["id"]
        return None

    def get_result_data(self, result_id):
        if self.__cursor:
            self.__cursor.execute("SELECT * FROM results WHERE id=%s",
                                  (result_id,))
            user_data = self.__cursor.fetchone()
            if user_data:
                return user_data
        return None

    def get_all_results(self, user_id):
        if self.__cursor:
            self.__cursor.execute("SELECT id FROM results WHERE user_id=%s",
                                  (user_id,))
            user_data = self.__cursor.fetchall()
            return user_data
        return None

    def delete_result(self, result_id):
        if self.__cursor:
            self.__cursor.execute("DELETE FROM results WHERE id=%s",
                                  (result_id,))
            self.__conn.commit()
            return True
        return False

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

    def delete_all_records(self):
        """
        Функция, удаляющая все записи в базе данных.

        :return: True или False.
        """
        if self.__cursor:
            self.__cursor.execute("DELETE FROM results")
            self.__cursor.execute("DELETE FROM deconvolution_jobs")
            self.__cursor.execute("DELETE FROM users")
            self.__conn.commit()
            return True
        return False

    def close_connection(self):
        """
        Функция закрытия соединения с базой данных.

        :return: None.
        """
        self.__cursor.close()
        self.__conn.close()
