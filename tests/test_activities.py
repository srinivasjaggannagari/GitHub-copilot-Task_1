"""
Tests for the activities endpoint.

Tests that the GET /activities endpoint returns the correct activity data.
"""


def test_get_activities_returns_all_activities(client, fresh_activities):
    """
    Test that GET /activities returns all activities
    
    AAA Pattern:
    - Arrange: We know what activities should be returned
    - Act: Make GET request to /activities
    - Assert: Verify response contains all activities with correct structure
    """
    # Arrange
    expected_activities = fresh_activities
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify all expected activities are in response
    for activity_name in expected_activities.keys():
        assert activity_name in data
    
    # Verify the response matches the expected structure
    assert data == expected_activities


def test_get_activities_has_correct_structure(client, fresh_activities):
    """
    Test that each activity in GET /activities has the correct fields
    
    AAA Pattern:
    - Arrange: We know the required structure for each activity
    - Act: Make GET request to /activities
    - Assert: Verify each activity has all required fields
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_participants_are_correct(client, fresh_activities):
    """
    Test that participants list matches expected values
    
    AAA Pattern:
    - Arrange: We know the initial participants for each activity
    - Act: Make GET request to /activities
    - Assert: Verify participants match expectations
    """
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["Chess Club"]["participants"] == expected_chess_participants
