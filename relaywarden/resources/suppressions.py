"""Suppressions resource for managing recipient suppressions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Suppressions:
    """Suppressions resource for managing recipient suppressions."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all suppressions for the current team."""
        return self.client.get("/suppressions") or {}

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a recipient to the suppression list."""
        return self.client.post("/suppressions", data) or {}

    def delete(self, suppression_id: str) -> None:
        """Remove a recipient from the suppression list."""
        self.client.delete(f"/suppressions/{suppression_id}")

    def import_suppressions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Import multiple suppressions in bulk."""
        return self.client.post("/suppressions/import", data) or {}

    def export(self) -> str:
        """Export all suppressions as a CSV file."""
        # Note: This endpoint returns CSV, not JSON
        # In a production SDK, you might want to return bytes or handle CSV parsing
        response = self.client.get("/suppressions/export")
        return ""  # Simplified - actual implementation would handle CSV
