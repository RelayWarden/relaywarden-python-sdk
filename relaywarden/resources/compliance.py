"""Compliance resource for managing data retention and compliance settings."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from relaywarden.client import Client


class Compliance:
    """Compliance resource for managing data retention and compliance settings."""

    def __init__(self, client: Client):
        self.client = client

    def get_retention(self) -> Dict[str, Any]:
        """Get data retention settings for the current team."""
        return self.client.get("/compliance/retention") or {}

    def update_retention(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update data retention settings."""
        return self.client.patch("/compliance/retention", data) or {}

    def get_export_config(self) -> Dict[str, Any]:
        """Get available export formats and configuration."""
        return self.client.get("/compliance/exports/config") or {}
