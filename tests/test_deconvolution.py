from fastapi.testclient import TestClient

from tests.utils.preparation import register
from app.main import app

client = TestClient(app)
headers = None
result_id = None


def test_calculate():
    global headers
    headers = register(client)

    data = {
        "base64_img": ""
    }

    response = client.post("/deconvolution/calculate",
                           json=data,
                           headers=headers)
    assert response.status_code == 400

    with open("resources/image_base64.txt", "r") as file:
        data["base64_img"] = file.read()

    response = client.post("/deconvolution/calculate",
                           json=data)
    assert response.status_code == 401

    response = client.post("/deconvolution/calculate",
                           json=data,
                           headers=headers)
    assert response.status_code == 200
    global result_id
    result_id = response.json()["result_id"]


def test_watch():
    global headers
    global result_id
    response = client.get("/deconvolution/watch/0",
                          headers=headers)
    assert response.status_code == 400

    response = client.get(f"/deconvolution/watch/{result_id}",
                          headers=headers)
    assert response.status_code == 200

    response = client.get(f"/deconvolution/watch/{result_id}")
    assert response.status_code == 401


def test_get_results():
    global headers

    response = client.get("/deconvolution/results",
                          headers=headers)
    assert response.status_code == 200

    response = client.get("/deconvolution/results")
    assert response.status_code == 401


def test_delete_result():
    global headers
    global result_id
    response = client.delete("/deconvolution/delete_result/0",
                             headers=headers)
    assert response.status_code == 400

    response = client.delete(f"/deconvolution/delete_result/{result_id}",
                             headers=headers)
    assert response.status_code == 200

    response = client.delete(f"/deconvolution/delete_result/{result_id}")
    assert response.status_code == 401
