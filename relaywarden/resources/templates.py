"""Templates resource for managing email templates."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Templates:
    """Templates resource for managing email templates."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all templates for the current project."""
        return self.client.get("/templates") or {}

    def get(self, template_id: str) -> Dict[str, Any]:
        """Get a specific template by ID."""
        return self.client.get(f"/templates/{template_id}") or {}

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new template."""
        return self.client.post("/templates", data) or {}

    def update(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a template."""
        return self.client.patch(f"/templates/{template_id}", data) or {}

    def delete(self, template_id: str) -> None:
        """Delete a template."""
        self.client.delete(f"/templates/{template_id}")

    def list_versions(
        self, template_id: str, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """List all versions of a template."""
        return self.client.get(f"/templates/{template_id}/versions") or {}

    def create_version(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new version of a template."""
        return self.client.post(f"/templates/{template_id}/versions", data) or {}

    def render(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a template with provided data."""
        return self.client.post(f"/templates/{template_id}/render", data) or {}

    def test_send(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a test email using the template."""
        return self.client.post(f"/templates/{template_id}/test-send", data) or {}
