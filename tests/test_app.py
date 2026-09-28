import os

os.environ["REDIS_HOST"] = "localhost"

from app.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Evaluation DevOps"


def test_visits():
    client = app.test_client()

    response = client.get("/visits")

    assert response.status_code == 200
    assert "visits" in response.get_json()
