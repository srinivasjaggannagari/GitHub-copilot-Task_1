"""
Pytest configuration and shared fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.app import app, activities


@pytest.fixture
def client():
    """
    Create a TestClient for the FastAPI app.
    
    Provides a test client that can make HTTP requests to the app
    without running a live server.
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a fresh copy of activities for each test.
    
    This ensures test isolation by giving each test its own copy
    of the activity data, preventing tests from interfering with each other.
    """
    # Create a deep copy to avoid modifying the original
    return deepcopy(activities)


@pytest.fixture
def sample_data():
    """
    Provide commonly used test data.
    
    A fixture with known activity names, emails, and expected values
    for use in tests.
    """
    return {
        "valid_activity": "Chess Club",
        "invalid_activity": "Nonexistent Activity",
        "valid_email": "newstudent@mergington.edu",
        "existing_email": "michael@mergington.edu",
        "another_email": "teststudent@mergington.edu",
    }


@pytest.fixture(autouse=True)
def mock_activities(fresh_activities, monkeypatch):
    """
    Replace the app's activities dict with fresh_activities for each test.
    
    This fixture automatically runs for every test (autouse=True) and ensures
    that the app uses the fresh copy of activities. The monkeypatch fixture
    temporarily replaces the original activities.
    """
    import src.app
    monkeypatch.setattr(src.app, "activities", fresh_activities)
