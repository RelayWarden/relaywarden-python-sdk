"""Senders resource for managing sender addresses."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Senders:
    """Senders resource for managing sender addresses."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all sender addresses for the current project."""
        return self.client.get("/senders") or {}

    def get(self, sender_id: str) -> Dict[str, Any]:
        """Get a specific sender by ID."""
        return self.client.get(f"/senders/{sender_id}") or {}

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new sender address."""
        return self.client.post("/senders", data) or {}

    def delete(self, sender_id: str) -> None:
        """Delete a sender address."""
        self.client.delete(f"/senders/{sender_id}")

    def verify(self, sender_id: str) -> Dict[str, Any]:
        """Initiate sender verification."""
        return self.client.post(f"/senders/{sender_id}/verify") or {}
