"""Service Accounts resource for managing service accounts and tokens."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class ServiceAccounts:
    """Service Accounts resource for managing service accounts and tokens."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all service accounts for the current team."""
        return self.client.get("/service-accounts") or {}

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new service account."""
        return self.client.post("/service-accounts", data) or {}

    def delete(self, service_account_id: str) -> None:
        """Delete a service account."""
        self.client.delete(f"/service-accounts/{service_account_id}")

    def create_token(
        self, service_account_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new API token for a service account."""
        return self.client.post(
            f"/service-accounts/{service_account_id}/tokens", data
        ) or {}

    def delete_token(self, token_id: str) -> None:
        """Delete an API token."""
        self.client.delete(f"/tokens/{token_id}")
