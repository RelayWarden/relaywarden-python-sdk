"""Domains resource for managing sending domains."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Domains:
    """Domains resource for managing sending domains."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all sending domains for the current project."""
        return self.client.get("/domains") or {}

    def get(self, domain_id: str) -> Dict[str, Any]:
        """Get a specific domain by ID."""
        return self.client.get(f"/domains/{domain_id}") or {}

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new sending domain."""
        return self.client.post("/domains", data) or {}

    def update(self, domain_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a domain."""
        return self.client.patch(f"/domains/{domain_id}", data) or {}

    def delete(self, domain_id: str) -> None:
        """Delete a domain."""
        self.client.delete(f"/domains/{domain_id}")

    def get_dns_records(self, domain_id: str) -> Dict[str, Any]:
        """Get DNS records required for domain verification."""
        return self.client.get(f"/domains/{domain_id}/dns-records") or {}

    def get_checks(self, domain_id: str) -> Dict[str, Any]:
        """Get current status of domain verification checks."""
        return self.client.get(f"/domains/{domain_id}/checks") or {}

    def verify(self, domain_id: str) -> Dict[str, Any]:
        """Initiate domain verification."""
        return self.client.post(f"/domains/{domain_id}/verify") or {}

    def rotate_dkim(self, domain_id: str) -> Dict[str, Any]:
        """Rotate DKIM signing keys for a domain."""
        return self.client.post(f"/domains/{domain_id}/dkim/rotate") or {}

    def enable_production(self, domain_id: str) -> Dict[str, Any]:
        """Enable a domain for production use."""
        return self.client.post(f"/domains/{domain_id}/enable-production") or {}
