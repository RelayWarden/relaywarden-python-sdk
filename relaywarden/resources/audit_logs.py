"""Audit Logs resource for viewing audit history."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class AuditLogs:
    """Audit Logs resource for viewing audit history."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List audit logs for the current team."""
        return self.client.get("/audit-logs") or {}

    def get(self, audit_log_id: str) -> Dict[str, Any]:
        """Get a specific audit log entry by ID."""
        return self.client.get(f"/audit-logs/{audit_log_id}") or {}
