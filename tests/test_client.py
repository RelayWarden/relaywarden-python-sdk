"""Tests for the RelayWarden client."""

import json
from unittest.mock import Mock, patch

import pytest

from relaywarden import Client
from relaywarden.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)


def test_client_initialization():
    """Test client initialization."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    assert client.base_url == "https://api.relaywarden.eu/api/v1"
    assert client.token == "test-token"


def test_set_project_id():
    """Test setting project ID."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    client.set_project_id("project-123")
    assert client.get_project_id() == "project-123"


def test_set_team_id():
    """Test setting team ID."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    client.set_team_id("team-123")
    assert client.get_team_id() == "team-123"


def test_get_request():
    """Test GET request."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    with patch.object(client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"id": "123", "name": "Test"},
            "meta": {"request_id": "req-123"},
        }
        mock_response.content = b'{"data":{"id":"123","name":"Test"},"meta":{"request_id":"req-123"}}'
        mock_request.return_value = mock_response

        result = client.get("/test")
        assert result is not None
        assert result["data"]["id"] == "123"


def test_post_request():
    """Test POST request."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    with patch.object(client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": {"id": "123"}}
        mock_response.content = b'{"data":{"id":"123"}}'
        mock_request.return_value = mock_response

        result = client.post("/test", {"name": "Test"})
        assert result is not None
        assert result["data"]["id"] == "123"


def test_authentication_error():
    """Test authentication error handling."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    with patch.object(client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"code": "unauthorized", "message": "Unauthenticated"},
            "meta": {"request_id": "req-123"},
        }
        mock_response.content = b'{"error":{"code":"unauthorized","message":"Unauthenticated"},"meta":{"request_id":"req-123"}}'
        mock_response.headers = {}
        mock_request.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            client.get("/test")
        assert exc_info.value.code == 401


def test_validation_error():
    """Test validation error handling."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    with patch.object(client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "error": {
                "code": "validation_error",
                "message": "Validation failed",
                "details": [{"field": "email", "message": "Invalid email"}],
            },
            "meta": {"request_id": "req-123"},
        }
        mock_response.content = b'{"error":{"code":"validation_error","message":"Validation failed","details":[{"field":"email","message":"Invalid email"}]},"meta":{"request_id":"req-123"}}'
        mock_response.headers = {}
        mock_request.return_value = mock_response

        with pytest.raises(ValidationError) as exc_info:
            client.post("/test", {})
        assert exc_info.value.code == 422
        assert len(exc_info.value.details) > 0


def test_rate_limit_error():
    """Test rate limit error handling."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    with patch.object(client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "error": {"code": "rate_limit_exceeded", "message": "Rate limit exceeded"},
            "meta": {"request_id": "req-123"},
        }
        mock_response.content = b'{"error":{"code":"rate_limit_exceeded","message":"Rate limit exceeded"},"meta":{"request_id":"req-123"}}'
        mock_response.headers = {"Retry-After": "60"}
        mock_request.return_value = mock_response

        with pytest.raises(RateLimitError) as exc_info:
            client.get("/test")
        assert exc_info.value.code == 429
        assert exc_info.value.retry_after == 60
