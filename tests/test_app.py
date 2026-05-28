import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def setup_function():
    # Reset the in-memory activities before each test
    for activity in activities.values():
        if isinstance(activity.get('participants'), list):
            activity['participants'].clear()
    # Repopulate with initial data
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Soccer Team"]["participants"] = ["alex@mergington.edu", "nina@mergington.edu"]
    activities["Basketball Club"]["participants"] = ["sam@mergington.edu", "mia@mergington.edu"]
    activities["Art Studio"]["participants"] = ["julia@mergington.edu", "noah@mergington.edu"]
    activities["Drama Club"]["participants"] = ["lucas@mergington.edu", "zara@mergington.edu"]
    activities["Debate Team"]["participants"] = ["grace@mergington.edu", "tyler@mergington.edu"]
    activities["Robotics Club"]["participants"] = ["natalie@mergington.edu", "owen@mergington.edu"]


def test_get_activities():
    # Arrange
    # (No special setup needed, uses default data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_nonexistent_activity():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
