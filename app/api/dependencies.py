from app.database.postgres import Database
from app.deconvolution.frt import Deconvolution


def get_database():
    database = Database()
    try:
        yield database
    finally:
        database.close_connection()


def get_deconvolutioner():
    return Deconvolution()
