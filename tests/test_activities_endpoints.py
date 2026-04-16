"""Integration tests for activity retrieval endpoints."""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities with correct structure."""
        # Arrange
        expected_activity_count = 3
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_returns_activity_details(self, client):
        """Test that each activity contains required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert all(field in activity_data for field in required_fields)
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_preserves_participants_list(self, client):
        """Test that participant lists are returned correctly."""
        # Arrange (test data includes Chess Club with 1 participant, Gym Class with 2)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert activities["Chess Club"]["participants"] == ["michael@mergington.edu"]
        assert len(activities["Gym Class"]["participants"]) == 2
        assert activities["Programming Class"]["participants"] == []


class TestRootRedirect:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_index(self, client):
        """Test that GET / redirects to /static/index.html."""
        # Arrange
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
