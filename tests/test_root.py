"""
Tests for the root endpoint.

Tests that the GET / endpoint properly redirects to /static/index.html
"""


def test_root_redirect(client):
    """
    Test that GET / redirects to /static/index.html
    
    AAA Pattern:
    - Arrange: Client is ready
    - Act: Make GET request to /
    - Assert: Verify status code is 307 (Temporary Redirect) and location header is correct
    """
    # Arrange - nothing special needed, client fixture is ready
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_follow(client):
    """
    Test that following the redirect from GET / leads to index.html
    
    AAA Pattern:
    - Arrange: Client is ready
    - Act: Make GET request to / with follow_redirects=True
    - Assert: Verify we get a 200 status (successfully retrieved the HTML page)
    """
    # Arrange - nothing special needed, client fixture is ready
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text
