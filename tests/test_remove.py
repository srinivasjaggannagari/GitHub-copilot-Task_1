"""
Tests for the remove endpoint.

Tests that the POST /activities/{activity_name}/remove endpoint correctly
handles removing students from activities, validation, and error cases.
"""


def test_remove_valid_participant(client, fresh_activities, sample_data):
    """
    Test that a registered participant can be removed from an activity (happy path)
    
    AAA Pattern:
    - Arrange: Prepare valid activity and existing participant
    - Act: Make POST request to remove endpoint
    - Assert: Verify response is successful and participant is removed
    """
    # Arrange
    activity_name = sample_data["valid_activity"]
    email = sample_data["existing_email"]  # This email is already registered
    initial_count = len(fresh_activities[activity_name]["participants"])
    assert email in fresh_activities[activity_name]["participants"]
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/remove?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count - 1


def test_remove_activity_not_found(client, sample_data):
    """
    Test that remove fails with 404 when activity doesn't exist
    
    AAA Pattern:
    - Arrange: Prepare invalid activity name and valid email
    - Act: Make POST request to remove endpoint with invalid activity
    - Assert: Verify response is 404 with appropriate error message
    """
    # Arrange
    activity_name = sample_data["invalid_activity"]
    email = sample_data["valid_email"]
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/remove?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_unregistered_student(client, fresh_activities, sample_data):
    """
    Test that removing a student not registered for an activity fails with 400
    
    AAA Pattern:
    - Arrange: Prepare valid activity and email that's not registered
    - Act: Attempt to remove the unregistered student
    - Assert: Verify response is 400 with appropriate error message
    """
    # Arrange
    activity_name = sample_data["valid_activity"]
    email = sample_data["valid_email"]  # This email is NOT registered
    assert email not in fresh_activities[activity_name]["participants"]
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/remove?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"
    # Verify participant count hasn't changed
    assert len(fresh_activities[activity_name]["participants"]) == initial_count


def test_remove_multiple_participants(client, fresh_activities):
    """
    Test that multiple participants can be removed from an activity
    
    AAA Pattern:
    - Arrange: Prepare an activity with multiple participants
    - Act: Remove several participants one by one
    - Assert: Verify each removal succeeds and final count is correct
    """
    # Arrange
    activity_name = "Chess Club"
    email1 = "michael@mergington.edu"
    email2 = "daniel@mergington.edu"
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response1 = client.post(f"/activities/{activity_name}/remove?email={email1}")
    response2 = client.post(f"/activities/{activity_name}/remove?email={email2}")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email1 not in fresh_activities[activity_name]["participants"]
    assert email2 not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count - 2


def test_signup_then_remove(client, fresh_activities):
    """
    Test the full lifecycle: sign up, then remove a participant
    
    AAA Pattern:
    - Arrange: Prepare activity and new student email
    - Act: Sign up student, then remove them
    - Assert: Verify both operations succeed and final state is correct
    """
    # Arrange
    activity_name = "Programming Class"
    email = "lifecycletest@test.edu"
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act - Sign up
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in fresh_activities[activity_name]["participants"]
    
    # Act - Remove
    remove_response = client.post(f"/activities/{activity_name}/remove?email={email}")
    
    # Assert
    assert remove_response.status_code == 200
    assert email not in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count
