from fastapi.testclient import TestClient

from app.database.postgres import Database
from app.main import app

client = TestClient(app)


def test_registration():
    database = Database()
    database.delete_all_records()

    data = {
        "username": "test_user",
        "password": "test_user",
        "retyped_password": "INCORRECT_SECOND_PASSWORD",
        "email": "test_user@mail.ru"
    }
    response = client.post("/auth/sign_up",
                           json=data)
    assert response.status_code == 400

    data['retyped_password'] = "test_user"
    response = client.post("/auth/sign_up",
                           json=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert "id" in response.json()
    assert "username" in response.json()

    response = client.post("/auth/sign_up",
                           json=data)
    assert response.status_code == 400

    database.close_connection()


def test_authorization():
    data = {
        "username": "test_user1",
        "password": "test_user"
    }
    response = client.post("/auth/sign_in",
                           data=data)
    assert response.status_code == 400

    data["username"] = "test_user"
    data["password"] = "test_user!!!"
    response = client.post("/auth/sign_in",
                           data=data)
    assert response.status_code == 401

    data["password"] = "test_user"
    response = client.post("/auth/sign_in",
                           data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
