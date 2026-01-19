"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock

from relaywarden import Client


@pytest.fixture
def client():
    """Create a test client."""
    return Client("https://api.relaywarden.eu/api/v1", "test-token")


@pytest.fixture
def mock_response():
    """Create a mock response."""
    response = Mock()
    response.status_code = 200
    response.content = b'{"data":{},"meta":{"request_id":"req-123"}}'
    response.headers = {}
    return response
