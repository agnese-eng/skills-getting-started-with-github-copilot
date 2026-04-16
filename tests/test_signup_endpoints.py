"""Integration tests for activity signup endpoint."""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_successful_signup(self, client):
        """Test that a student can successfully sign up for an activity."""
        # Arrange
        activity_name = "Programming Class"
        email = "alex@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    def test_signup_adds_participant_to_activity(self, client):
        """Test that participant is added to activity's participant list."""
        # Arrange
        activity_name = "Programming Class"
        email = "alex@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 1

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """Test that signing up for non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}

    def test_duplicate_signup_returns_400(self, client):
        """Test that registering twice for same activity is rejected."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered for Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Student is already signed up for this activity"
        }

    def test_duplicate_signup_does_not_add_duplicate(self, client):
        """Test that duplicate signup attempt doesn't add duplicate participants."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        participant_list = activities[activity_name]["participants"]
        assert participant_list.count(email) == 1  # Only one instance

    def test_multiple_different_students_can_signup(self, client):
        """Test that different students can all sign up for same activity."""
        # Arrange
        activity_name = "Programming Class"
        students = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        
        # Act
        for student in students:
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": student}
            )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        for student in students:
            assert student in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 3
