import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to sys.path to allow importing from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app("testing")
    app.config.from_object(TestingConfig)
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    # Return app context
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def mock_login_success(monkeypatch):
    """Mock a successful login response."""
    # Create mock function with the return value we want
    mock = MagicMock(return_value=(True, "fake-jwt-token", None))

    # Patch both possible import paths to be safe
    monkeypatch.setattr("app.utils.api.login_user", mock)
    monkeypatch.setattr("app.auth.routes.login_user", mock)

    return mock


@pytest.fixture
def mock_login_failure(monkeypatch):
    """Mock a failed login response."""
    # Create mock function with the return value we want
    mock = MagicMock(return_value=(False, None, "Invalid credentials"))

    # Patch both possible import paths to be safe
    monkeypatch.setattr("app.utils.api.login_user", mock)
    monkeypatch.setattr("app.auth.routes.login_user", mock)

    return mock


@pytest.fixture
def mock_register_success(monkeypatch):
    """Mock a successful registration response."""
    # Create mock function with the return value we want
    mock = MagicMock(return_value=(True, "Registration successful"))

    # Patch both possible import paths to be safe
    monkeypatch.setattr("app.utils.api.register_user", mock)
    monkeypatch.setattr("app.auth.routes.register_user", mock)

    return mock


@pytest.fixture
def mock_register_failure(monkeypatch):
    """Mock a failed registration response."""
    # Create mock function with the return value we want
    mock = MagicMock(return_value=(False, "Username already exists"))

    # Patch both possible import paths to be safe
    monkeypatch.setattr("app.utils.api.register_user", mock)
    monkeypatch.setattr("app.auth.routes.register_user", mock)

    return mock


@pytest.fixture
def mock_health_data(monkeypatch):
    """Mock the health data response."""
    # Create sample dataset response
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

    # Create the mock
    mock = MagicMock(return_value=(True, sample_data, None))

    # Patch both possible import paths
    monkeypatch.setattr("app.utils.api.get_acceleration_data", mock)
    monkeypatch.setattr("app.dashboard.routes.get_acceleration_data", mock)

    return mock


@pytest.fixture
def mock_no_health_data():
    """Mock an empty health data response."""
    with patch("app.utils.api.get_acceleration_data") as mock:
        mock.return_value = (True, [], None)
        yield mock


@pytest.fixture
def mock_health_data_error():
    """Mock an error in health data response."""
    with patch("app.utils.api.get_acceleration_data") as mock:
        mock.return_value = (False, None, "Failed to retrieve data")
        yield mock
