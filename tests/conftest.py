"""Pytest configuration and fixtures for API tests."""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_activities():
    """Fixture providing a clean copy of test activities data.
    
    Returns a minimal set of activities for testing purposes.
    Each test gets its own copy to ensure isolation.
    """
    return deepcopy({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    })


@pytest.fixture
def client(test_activities, monkeypatch):
    """Fixture providing a TestClient with isolated test data.
    
    Monkeypatches the app's activities dict with test data,
    ensuring each test runs with a clean state.
    """
    monkeypatch.setattr("src.app.activities", test_activities)
    return TestClient(app)
