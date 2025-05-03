from app.database.postgres import Database


def register(client):
    database = Database()
    database.delete_all_records()
    database.close_connection()

    data = {
        "username": "test_user",
        "password": "test_user",
        "retyped_password": "test_user",
        "email": "test_user@mail.ru"
    }
    response = client.post("/auth/sign_up",
                           json=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert "id" in response.json()
    assert "username" in response.json()

    data = {
        "username": "test_user",
        "password": "test_user"
    }
    response = client.post("/auth/sign_in",
                           data=data)
    assert response.status_code == 200

    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    return headers
