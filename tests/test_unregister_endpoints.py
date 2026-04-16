"""Integration tests for activity unregister endpoint."""

import pytest


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_successful_unregister(self, client):
        """Test that a student can successfully unregister from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    def test_unregister_removes_participant_from_activity(self, client):
        """Test that participant is removed from activity's participant list."""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Already registered in test data
        
        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 1  # One left

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}

    def test_unregister_nonexistent_participant_returns_400(self, client):
        """Test that unregistering a non-participant returns 400."""
        # Arrange
        activity_name = "Programming Class"
        email = "notregistered@mergington.edu"  # Not in Programming Class
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Student is not signed up for this activity"
        }

    def test_unregister_does_not_remove_wrong_participant(self, client):
        """Test that unregistering one participant doesn't affect others."""
        # Arrange
        activity_name = "Gym Class"
        participant_to_remove = "john@mergington.edu"
        participant_to_keep = "olivia@mergington.edu"
        
        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": participant_to_remove}
        )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert participant_to_remove not in activities[activity_name]["participants"]
        assert participant_to_keep in activities[activity_name]["participants"]

    def test_unregister_then_signup_again(self, client):
        """Test that a student can unregister and then sign up again."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act - Unregister
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        
        # Assert
        assert signup_response.status_code == 200
        activities = response.json()
        assert email in activities[activity_name]["participants"]
