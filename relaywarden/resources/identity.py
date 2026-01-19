"""Identity resource for user/team information."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Identity:
    """Identity resource for user/team information."""

    def __init__(self, client: Client):
        self.client = client

    def me(self) -> Dict[str, Any]:
        """
        Get information about the currently authenticated user or service account.

        Returns:
            User or service account information
        """
        return self.client.get("/me") or {}

    def teams(self) -> Dict[str, Any]:
        """
        List all teams the authenticated user belongs to.

        Returns:
            List of teams
        """
        return self.client.get("/teams") or {}
