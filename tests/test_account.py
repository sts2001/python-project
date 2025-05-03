from fastapi.testclient import TestClient

from tests.utils.preparation import register
from app.main import app

client = TestClient(app)
headers = None


def test_change_username():
    global headers
    headers = register(client)

    data = {
        "new_username": ""
    }

    response = client.put("/account/change_username",
                          json=data,
                          headers=headers)
    assert response.status_code == 400

    response = client.put("/account/change_username",
                          json=data)
    assert response.status_code == 401

    data["new_username"] = "I_TEST_USER"
    response = client.put("/account/change_username",
                          json=data,
                          headers=headers)
    assert response.status_code == 200


def test_change_password():
    global headers

    data = {
        "previous": "test_user",
        "new": "TEST_USER",
        "new_retyped": "TEST"
    }

    response = client.put("/account/change_password",
                          json=data,
                          headers=headers)
    assert response.status_code == 400

    data = {}
    response = client.put("/account/change_password",
                          json=data,
                          headers=headers)
    assert response.status_code == 422

    data = {
        "previous": "test_user",
        "new": "TEST_USER",
        "new_retyped": "TEST_USER"
    }
    response = client.put("/account/change_password",
                          json=data)
    assert response.status_code == 401

    response = client.put("/account/change_password",
                          json=data,
                          headers=headers)
    assert response.status_code == 200


def test_get_user_data():
    global headers

    response = client.get("/account/get_user_data")
    assert response.status_code == 401

    response = client.get("/account/get_user_data",
                          headers=headers)
    assert response.status_code == 200


def test_delete_account():
    global headers

    response = client.delete("/account/delete_account")
    assert response.status_code == 401

    response = client.delete("/account/delete_account",
                             headers=headers)
    assert response.status_code == 200
