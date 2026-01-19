"""Tests for resource classes."""

from unittest.mock import Mock, patch

import pytest

from relaywarden import Client
from relaywarden.resources.messages import Messages


def test_messages_send():
    """Test sending a message."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    client.set_project_id("project-123")
    messages = Messages(client)

    with patch.object(client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 202
        mock_response.json.return_value = {
            "data": {"message_id": "msg-123", "status": "accepted"},
            "meta": {"request_id": "req-123"},
        }
        mock_response.content = b'{"data":{"message_id":"msg-123","status":"accepted"},"meta":{"request_id":"req-123"}}'
        mock_request.return_value = mock_response

        result = messages.send(
            {
                "from": {"email": "noreply@example.com"},
                "to": [{"email": "user@example.com"}],
                "subject": "Test",
                "html": "<h1>Test</h1>",
            }
        )
        assert result["data"]["message_id"] == "msg-123"


def test_messages_list():
    """Test listing messages."""
    client = Client("https://api.relaywarden.eu/api/v1", "test-token")
    client.set_project_id("project-123")
    messages = Messages(client)

    with patch.object(client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"id": "msg-1", "subject": "Test 1"}],
            "meta": {"current_page": 1, "per_page": 25, "total": 1},
        }
        mock_response.content = b'{"data":[{"id":"msg-1","subject":"Test 1"}],"meta":{"current_page":1,"per_page":25,"total":1}}'
        mock_request.return_value = mock_response

        result = messages.list()
        assert len(result["data"]) == 1
