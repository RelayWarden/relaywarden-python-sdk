"""Messages resource for sending and managing email messages."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Messages:
    """Messages resource for sending and managing email messages."""

    def __init__(self, client: Client):
        self.client = client

    def send(
        self, data: Dict[str, Any], idempotency_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email message.

        Args:
            data: Message data
            idempotency_key: Optional idempotency key

        Returns:
            Message response
        """
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return self.client.post("/messages", data, headers) or {}

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all messages for the current project.

        Args:
            filters: Optional query parameters

        Returns:
            List of messages
        """
        return self.client.get("/messages") or {}

    def get(self, message_id: str) -> Dict[str, Any]:
        """
        Get a specific message by ID.

        Args:
            message_id: Message UUID

        Returns:
            Message information
        """
        return self.client.get(f"/messages/{message_id}") or {}

    def get_timeline(self, message_id: str) -> Dict[str, Any]:
        """
        Get the complete timeline of events for a message.

        Args:
            message_id: Message UUID

        Returns:
            Message timeline
        """
        return self.client.get(f"/messages/{message_id}/timeline") or {}

    def cancel(self, message_id: str) -> Dict[str, Any]:
        """
        Cancel a message that hasn't been sent yet.

        Args:
            message_id: Message UUID

        Returns:
            Cancelled message
        """
        return self.client.post(f"/messages/{message_id}/cancel") or {}

    def resend(self, message_id: str) -> Dict[str, Any]:
        """
        Resend a previously sent message.

        Args:
            message_id: Message UUID

        Returns:
            Resent message
        """
        return self.client.post(f"/messages/{message_id}/resend") or {}
