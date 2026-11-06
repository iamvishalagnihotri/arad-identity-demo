from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "ARAD Identity Demo" in response.text


def test_profile_requires_login():
    response = client.get("/me")
    assert response.status_code == 401
