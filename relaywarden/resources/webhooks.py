"""Webhooks resource for managing webhook endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Webhooks:
    """Webhooks resource for managing webhook endpoints."""

    def __init__(self, client: Client):
        self.client = client

    def list_endpoints(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """List all webhook endpoints for the current project."""
        return self.client.get("/webhooks/endpoints") or {}

    def create_endpoint(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new webhook endpoint."""
        return self.client.post("/webhooks/endpoints", data) or {}

    def update_endpoint(
        self, endpoint_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a webhook endpoint."""
        return self.client.patch(f"/webhooks/endpoints/{endpoint_id}", data) or {}

    def delete_endpoint(self, endpoint_id: str) -> None:
        """Delete a webhook endpoint."""
        self.client.delete(f"/webhooks/endpoints/{endpoint_id}")

    def list_deliveries(
        self, endpoint_id: str, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """List all delivery attempts for a webhook endpoint."""
        return self.client.get(f"/webhooks/endpoints/{endpoint_id}/deliveries") or {}

    def test_endpoint(self, endpoint_id: str) -> Dict[str, Any]:
        """Send a test webhook to verify the endpoint is working."""
        return self.client.post(f"/webhooks/endpoints/{endpoint_id}/test") or {}

    def replay_delivery(self, delivery_id: str) -> Dict[str, Any]:
        """Replay a failed webhook delivery."""
        return self.client.post(f"/webhooks/deliveries/{delivery_id}/replay") or {}
