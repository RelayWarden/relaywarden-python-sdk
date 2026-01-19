"""Events resource for viewing event history."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Events:
    """Events resource for viewing event history."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all events for the current team."""
        return self.client.get("/events") or {}

    def get(self, event_id: str) -> Dict[str, Any]:
        """Get a specific event by ID."""
        return self.client.get(f"/events/{event_id}") or {}
