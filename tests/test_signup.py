"""
Tests for the signup endpoint.

Tests that the POST /activities/{activity_name}/signup endpoint correctly
handles student registrations, validation, and error cases.
"""


def test_signup_valid_student(client, fresh_activities, sample_data):
    """
    Test that a valid student can sign up for an activity (happy path)
    
    AAA Pattern:
    - Arrange: Prepare valid activity name and email
    - Act: Make POST request to signup endpoint
    - Assert: Verify response is successful and participant is added
    """
    # Arrange
    activity_name = sample_data["valid_activity"]
    email = sample_data["valid_email"]
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in fresh_activities[activity_name]["participants"]
    assert len(fresh_activities[activity_name]["participants"]) == initial_count + 1


def test_signup_activity_not_found(client, sample_data):
    """
    Test that signup fails with 404 when activity doesn't exist
    
    AAA Pattern:
    - Arrange: Prepare invalid activity name and valid email
    - Act: Make POST request to signup endpoint with invalid activity
    - Assert: Verify response is 404 with appropriate error message
    """
    # Arrange
    activity_name = sample_data["invalid_activity"]
    email = sample_data["valid_email"]
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student(client, fresh_activities, sample_data):
    """
    Test that a student cannot sign up twice for the same activity
    
    AAA Pattern:
    - Arrange: Use a student that's already registered for an activity
    - Act: Attempt to sign up the same student again
    - Assert: Verify response is 400 with appropriate error message
    """
    # Arrange
    activity_name = sample_data["valid_activity"]
    email = sample_data["existing_email"]  # This email is already in Chess Club
    initial_count = len(fresh_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
    # Verify participant count hasn't changed
    assert len(fresh_activities[activity_name]["participants"]) == initial_count


def test_signup_multiple_students_different_activities(client, fresh_activities):
    """
    Test that multiple students can sign up for different activities
    
    AAA Pattern:
    - Arrange: Prepare two different activities and new students
    - Act: Sign up different students to different activities
    - Assert: Verify both signups succeed and participants are added correctly
    """
    # Arrange
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    email1 = "student1@test.edu"
    email2 = "student2@test.edu"
    
    # Act
    response1 = client.post(f"/activities/{activity1}/signup?email={email1}")
    response2 = client.post(f"/activities/{activity2}/signup?email={email2}")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email1 in fresh_activities[activity1]["participants"]
    assert email2 in fresh_activities[activity2]["participants"]
    assert email1 not in fresh_activities[activity2]["participants"]
    assert email2 not in fresh_activities[activity1]["participants"]


def test_signup_same_student_different_activities(client, fresh_activities):
    """
    Test that the same student can sign up for multiple different activities
    
    AAA Pattern:
    - Arrange: Prepare two different activities and one new student
    - Act: Sign up the same student to both activities
    - Assert: Verify both signups succeed and student is in both activities
    """
    # Arrange
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    email = "multiactivity@test.edu"
    
    # Act
    response1 = client.post(f"/activities/{activity1}/signup?email={email}")
    response2 = client.post(f"/activities/{activity2}/signup?email={email}")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email in fresh_activities[activity1]["participants"]
    assert email in fresh_activities[activity2]["participants"]
