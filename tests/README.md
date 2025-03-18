# Areum Health Visualization Tests

This directory contains automated tests for the Areum Health Visualization application. The tests ensure that all components of the application work correctly, even as new features are added.

## Test Structure

- `conftest.py` - Contains shared pytest fixtures
- `test_auth.py` - Tests for authentication (login/registration)
- `test_dashboard.py` - Tests for the dashboard functionality
- `test_utils.py` - Tests for utility functions (API, charts, data processing)

## Running Tests Locally

To run the tests locally:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app

# Run a specific test file
pytest tests/test_auth.py
```

## Test Fixtures

The test suite uses fixtures to mock external dependencies like API calls. This allows us to test the application without requiring a connection to the actual backend service.

Key fixtures include:

- `app` - Flask application configured for testing
- `client` - Flask test client
- `mock_login_success`/`mock_login_failure` - Mock successful/failed login responses
- `mock_register_success`/`mock_register_failure` - Mock successful/failed registration responses
- `mock_health_data` - Mock acceleration data responses

## Continuous Integration

These tests are automatically run in GitHub Actions when:
- Code is pushed to the main branch
- A pull request is created or updated

The CI pipeline runs tests, linting, and builds the Docker image if all tests pass.

## Adding New Tests

When adding new features to the application, be sure to add corresponding tests:

1. For new routes, add tests in the appropriate test file
2. For new utility functions, add tests in `test_utils.py`
3. If adding a new module, create a new test file named `test_modulename.py`

## Code Coverage

We aim to maintain high test coverage. To check coverage:

```bash
pytest --cov=app --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov` directory.