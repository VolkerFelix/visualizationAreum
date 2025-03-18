from unittest.mock import MagicMock
import pytest
from flask import session, url_for


def test_login_page_loads(client):
    """Test that the login page loads correctly."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login to View Your Health Data" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_register_page_loads(client):
    """Test that the register page loads correctly."""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create an Account" in response.data
    assert b"Username" in response.data
    assert b"Email Address" in response.data
    assert b"Password" in response.data


def test_successful_login(client, monkeypatch):
    """Test successful login with correct credentials."""
    # Create a mock login function
    mock_login = MagicMock(return_value=(True, "fake-jwt-token", None))

    # Apply the mock to the exact import path used in your routes
    monkeypatch.setattr("app.auth.routes.login_user", mock_login)

    response = client.post(
        "/login",
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )

    # Check login was successful
    assert response.status_code == 200
    mock_login.assert_called_once_with("testuser", "password123")

    # Should be redirected to dashboard
    assert b"Health Data Dashboard" in response.data

    # Session should contain token
    with client.session_transaction() as sess:
        assert "token" in sess


def test_failed_login(client, mock_login_failure):
    """Test failed login with incorrect credentials."""
    response = client.post(
        "/login",
        data={"username": "wronguser", "password": "wrongpass"},
        follow_redirects=True,
    )

    # Check login failed
    assert response.status_code == 200
    mock_login_failure.assert_called_once_with("wronguser", "wrongpass")

    # Should stay on login page with error
    assert b"Login to View Your Health Data" in response.data
    assert b"Invalid credentials" in response.data

    # Session should not contain token
    with client.session_transaction() as sess:
        assert "token" not in sess


def test_successful_registration(client, mock_register_success, mock_login_success):
    """Test successful user registration."""
    response = client.post(
        "/register",
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        },
        follow_redirects=True,
    )

    # Check registration was successful
    assert response.status_code == 200
    mock_register_success.assert_called_once_with(
        "newuser", "password123", "newuser@example.com"
    )

    # Check automatic login occurred
    mock_login_success.assert_called_once_with("newuser", "password123")

    # Should be redirected to dashboard
    assert b"Health Data Dashboard" in response.data

    # Session should contain token
    with client.session_transaction() as sess:
        assert "token" in sess


def test_failed_registration(client, mock_register_failure):
    """Test failed user registration."""
    response = client.post(
        "/register",
        data={
            "username": "existinguser",
            "email": "existinguser@example.com",
            "password": "password123",
        },
        follow_redirects=True,
    )

    # Check registration failed
    assert response.status_code == 200
    mock_register_failure.assert_called_once_with(
        "existinguser", "password123", "existinguser@example.com"
    )

    # Should stay on registration page with error
    assert b"Create an Account" in response.data
    assert b"Registration failed" in response.data
    assert b"Username already exists" in response.data

    # Session should not contain token
    with client.session_transaction() as sess:
        assert "token" not in sess


def test_registration_validation(client, mock_register_success):
    """Test form validation during registration."""
    # Test with too short password
    response = client.post(
        "/register",
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "short",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Password must be at least 8 characters long" in response.data
    mock_register_success.assert_not_called()

    # Test with missing fields
    response = client.post(
        "/register",
        data={
            "username": "newuser",
            "email": "",  # Empty email
            "password": "password123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"All fields are required" in response.data
    mock_register_success.assert_not_called()


def test_logout(client, mock_login_success):
    """Test that logout works correctly."""
    # First login
    client.post("/login", data={"username": "testuser", "password": "password123"})

    # Check session has token
    with client.session_transaction() as sess:
        assert "token" in sess

    # Now logout
    response = client.get("/logout", follow_redirects=True)

    # Check logout worked
    assert response.status_code == 200
    assert b"You have been logged out" in response.data
    assert b"Login to View Your Health Data" in response.data

    # Session should not contain token
    with client.session_transaction() as sess:
        assert "token" not in sess
