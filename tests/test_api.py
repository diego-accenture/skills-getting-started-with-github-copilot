import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_returns_all_activities(client):
    # Arrange
    # (No special setup needed for in-memory activities)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity_success(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_for_activity_already_signed_up(client):
    # Arrange
    email = "dupeuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_for_nonexistent_activity(client):
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Nonexistent Activity"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
