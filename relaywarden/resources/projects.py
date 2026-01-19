"""Projects resource for managing projects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from relaywarden.client import Client


class Projects:
    """Projects resource for managing projects."""

    def __init__(self, client: Client):
        self.client = client

    def list(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all projects for the current team.

        Args:
            filters: Optional query parameters

        Returns:
            List of projects
        """
        # Note: filters would need to be converted to query params in actual implementation
        return self.client.get("/projects") or {}

    def get(self, project_id: str) -> Dict[str, Any]:
        """
        Get a specific project by ID.

        Args:
            project_id: Project UUID

        Returns:
            Project information
        """
        return self.client.get(f"/projects/{project_id}") or {}

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project.

        Args:
            data: Project data

        Returns:
            Created project
        """
        return self.client.post("/projects", data) or {}

    def update(self, project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a project.

        Args:
            project_id: Project UUID
            data: Update data

        Returns:
            Updated project
        """
        return self.client.patch(f"/projects/{project_id}", data) or {}

    def delete(self, project_id: str) -> None:
        """
        Delete a project.

        Args:
            project_id: Project UUID
        """
        self.client.delete(f"/projects/{project_id}")
