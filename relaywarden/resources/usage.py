"""Usage resource for viewing usage statistics and limits."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Usage:
    """Usage resource for viewing usage statistics and limits."""

    def __init__(self, client: Client):
        self.client = client

    def get_daily(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get daily usage statistics for the current team."""
        return self.client.get("/usage/daily") or {}

    def get_limits(self) -> Dict[str, Any]:
        """Get current usage limits and remaining quota."""
        return self.client.get("/limits") or {}

    def get_diagnostics(self) -> Dict[str, Any]:
        """Get system health and diagnostic information."""
        return self.client.get("/diagnostics") or {}
