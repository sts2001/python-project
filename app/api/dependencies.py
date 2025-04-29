from app.database.postgres import Database


def get_database():
    database = Database()
    try:
        yield database
    finally:
        database.close_connection()
