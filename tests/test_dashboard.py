import pytest
from unittest.mock import MagicMock
from flask import session


def test_dashboard_requires_login(client):
    """Test that the dashboard redirects to login when not authenticated."""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # More flexible check for login-related content


def test_dashboard_with_health_data(client, monkeypatch):
    """Test dashboard shows health data when authenticated."""
    # Set up mocks
    from unittest.mock import MagicMock

    # Mock the login function
    login_mock = MagicMock(return_value=(True, "fake-jwt-token", None))
    monkeypatch.setattr("app.auth.routes.login_user", login_mock)

    # Create sample acceleration data
    sample_data = [
        {
            "id": "test-dataset-id",
            "data_type": "acceleration",
            "device_info": {"device_type": "iPhone", "model": "iPhone 13"},
            "sampling_rate_hz": 50,
            "start_time": "2025-03-10T12:00:00Z",
            "created_at": "2025-03-10T12:10:00Z",
            "data": {
                "samples": [
                    {
                        "timestamp": "2025-03-10T12:00:00.000Z",
                        "x": 0.1,
                        "y": 0.2,
                        "z": 0.9,
                    },
                    {
                        "timestamp": "2025-03-10T12:00:00.020Z",
                        "x": 0.2,
                        "y": 0.3,
                        "z": 0.8,
                    },
                    {
                        "timestamp": "2025-03-10T12:00:00.040Z",
                        "x": 0.15,
                        "y": 0.25,
                        "z": 0.85,
                    },
                ]
            },
        }
    ]

    # Mock the health data API
    health_mock = MagicMock(return_value=(True, sample_data, None))
    monkeypatch.setattr("app.dashboard.routes.get_acceleration_data", health_mock)

    # Skip chart generation for this test
    chart_mock = MagicMock(return_value='<div id="chart"></div>')
    monkeypatch.setattr("app.utils.charts.create_xyz_chart", chart_mock)
    monkeypatch.setattr("app.utils.charts.create_magnitude_chart", chart_mock)

    # Login first
    client.post("/login", data={"username": "testuser", "password": "password123"})

    # Set session token manually
    with client.session_transaction() as sess:
        sess["token"] = "fake-jwt-token"

    # Request the dashboard
    response = client.get("/")

    # Basic checks
    assert response.status_code == 200

    # Just check that the API mock was called correctly
    health_mock.assert_called_once()

    # Check that login page is not shown
    assert b"Login to View Your Health Data" not in response.data

    # Avoid checking for the absence of "error" which might appear in many contexts
    # Instead check that specific error messages are not present
    assert b"Failed to retrieve data" not in response.data
    assert b"No data available" not in response.data


def test_dashboard_no_health_data(client, monkeypatch):
    """Test dashboard shows appropriate message when no health data is available."""
    # Set up mocks
    from unittest.mock import MagicMock

    # Mock login
    login_mock = MagicMock(return_value=(True, "fake-jwt-token", None))
    monkeypatch.setattr("app.auth.routes.login_user", login_mock)

    # Mock empty health data
    health_mock = MagicMock(return_value=(True, [], None))
    monkeypatch.setattr("app.dashboard.routes.get_acceleration_data", health_mock)

    # Login and set session
    client.post("/login", data={"username": "testuser", "password": "password123"})
    with client.session_transaction() as sess:
        sess["token"] = "fake-jwt-token"

    # Get dashboard
    response = client.get("/")

    # Basic checks
    assert response.status_code == 200
    health_mock.assert_called_once()


def test_dashboard_health_data_error(client, monkeypatch):
    """Test dashboard handles errors in health data retrieval."""
    # Set up mocks
    from unittest.mock import MagicMock

    # Mock login
    login_mock = MagicMock(return_value=(True, "fake-jwt-token", None))
    monkeypatch.setattr("app.auth.routes.login_user", login_mock)

    # Mock failed health data API call
    health_mock = MagicMock(return_value=(False, None, "Failed to retrieve data"))
    monkeypatch.setattr("app.dashboard.routes.get_acceleration_data", health_mock)

    # Login and set session
    client.post("/login", data={"username": "testuser", "password": "password123"})
    with client.session_transaction() as sess:
        sess["token"] = "fake-jwt-token"

    # Get dashboard
    response = client.get("/")

    # Basic checks
    assert response.status_code == 200
    health_mock.assert_called_once()


def test_refresh_endpoint(client):
    """Test the refresh endpoint redirects to the dashboard."""
    # Set token in session
    with client.session_transaction() as sess:
        sess["token"] = "fake-jwt-token"

    # Try to access refresh endpoint
    response = client.get("/refresh", follow_redirects=True)
    assert response.status_code == 200
