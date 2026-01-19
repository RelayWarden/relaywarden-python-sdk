"""Main client for interacting with the RelayWarden API."""

import time
from typing import Any, Dict, Optional

import requests

from relaywarden.exceptions import APIError, AuthenticationError, RateLimitError, ValidationError
from relaywarden.resources.audit_logs import AuditLogs
from relaywarden.resources.compliance import Compliance
from relaywarden.resources.domains import Domains
from relaywarden.resources.events import Events
from relaywarden.resources.identity import Identity
from relaywarden.resources.messages import Messages
from relaywarden.resources.projects import Projects
from relaywarden.resources.senders import Senders
from relaywarden.resources.service_accounts import ServiceAccounts
from relaywarden.resources.suppressions import Suppressions
from relaywarden.resources.templates import Templates
from relaywarden.resources.usage import Usage
from relaywarden.resources.webhooks import Webhooks


class Client:
    """Main client for interacting with the RelayWarden API."""

    def __init__(
        self,
        base_url: str,
        token: str,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        """
        Initialize a new RelayWarden API client.

        Args:
            base_url: The base URL of the API (e.g., 'https://api.relaywarden.eu/api/v1')
            token: Your API token
            max_retries: Maximum number of retry attempts (default: 3)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.max_retries = max_retries
        self.timeout = timeout
        self.project_id: Optional[str] = None
        self.team_id: Optional[str] = None

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Initialize resources
        self._identity: Optional[Identity] = None
        self._projects: Optional[Projects] = None
        self._service_accounts: Optional[ServiceAccounts] = None
        self._domains: Optional[Domains] = None
        self._senders: Optional[Senders] = None
        self._templates: Optional[Templates] = None
        self._messages: Optional[Messages] = None
        self._events: Optional[Events] = None
        self._webhooks: Optional[Webhooks] = None
        self._suppressions: Optional[Suppressions] = None
        self._usage: Optional[Usage] = None
        self._audit_logs: Optional[AuditLogs] = None
        self._compliance: Optional[Compliance] = None

    def set_project_id(self, project_id: Optional[str]) -> None:
        """Set the project ID for project-scoped operations."""
        self.project_id = project_id

    def get_project_id(self) -> Optional[str]:
        """Get the current project ID."""
        return self.project_id

    def set_team_id(self, team_id: Optional[str]) -> None:
        """Set the team ID."""
        self.team_id = team_id

    def get_team_id(self) -> Optional[str]:
        """Get the current team ID."""
        return self.team_id

    @property
    def identity(self) -> Identity:
        """Access the Identity resource."""
        if self._identity is None:
            self._identity = Identity(self)
        return self._identity

    @property
    def projects(self) -> Projects:
        """Access the Projects resource."""
        if self._projects is None:
            self._projects = Projects(self)
        return self._projects

    @property
    def service_accounts(self) -> ServiceAccounts:
        """Access the ServiceAccounts resource."""
        if self._service_accounts is None:
            self._service_accounts = ServiceAccounts(self)
        return self._service_accounts

    @property
    def domains(self) -> Domains:
        """Access the Domains resource."""
        if self._domains is None:
            self._domains = Domains(self)
        return self._domains

    @property
    def senders(self) -> Senders:
        """Access the Senders resource."""
        if self._senders is None:
            self._senders = Senders(self)
        return self._senders

    @property
    def templates(self) -> Templates:
        """Access the Templates resource."""
        if self._templates is None:
            self._templates = Templates(self)
        return self._templates

    @property
    def messages(self) -> Messages:
        """Access the Messages resource."""
        if self._messages is None:
            self._messages = Messages(self)
        return self._messages

    @property
    def events(self) -> Events:
        """Access the Events resource."""
        if self._events is None:
            self._events = Events(self)
        return self._events

    @property
    def webhooks(self) -> Webhooks:
        """Access the Webhooks resource."""
        if self._webhooks is None:
            self._webhooks = Webhooks(self)
        return self._webhooks

    @property
    def suppressions(self) -> Suppressions:
        """Access the Suppressions resource."""
        if self._suppressions is None:
            self._suppressions = Suppressions(self)
        return self._suppressions

    @property
    def usage(self) -> Usage:
        """Access the Usage resource."""
        if self._usage is None:
            self._usage = Usage(self)
        return self._usage

    @property
    def audit_logs(self) -> AuditLogs:
        """Access the AuditLogs resource."""
        if self._audit_logs is None:
            self._audit_logs = AuditLogs(self)
        return self._audit_logs

    @property
    def compliance(self) -> Compliance:
        """Access the Compliance resource."""
        if self._compliance is None:
            self._compliance = Compliance(self)
        return self._compliance

    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers including project/team IDs."""
        headers = {}
        if self.project_id:
            headers["X-Project-Id"] = self.project_id
        if self.team_id:
            headers["X-Team-Id"] = self.team_id
        return headers

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            path: API path
            data: Request body data
            headers: Additional headers

        Returns:
            Response data or None for 204 responses

        Raises:
            APIError: For API errors
            AuthenticationError: For authentication failures
            ValidationError: For validation errors
            RateLimitError: For rate limit errors
        """
        url = f"{self.base_url}{path}"
        request_headers = {**self._get_default_headers(), **(headers or {})}

        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=request_headers,
                    timeout=self.timeout,
                )

                if response.status_code == 204:
                    return None

                if response.status_code >= 200 and response.status_code < 300:
                    if response.content:
                        return response.json()
                    return {}

                # Handle errors
                error_data = None
                if response.content:
                    try:
                        error_data = response.json()
                    except ValueError:
                        pass

                api_error = self._handle_error_response(response, error_data)

                # Retry on rate limit
                if isinstance(api_error, RateLimitError) and attempt < self.max_retries:
                    time.sleep(api_error.retry_after)
                    last_exception = api_error
                    continue

                raise api_error

            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < self.max_retries and self._is_retryable_error(e):
                    time.sleep(0.1 * (attempt + 1))  # Exponential backoff
                    continue
                raise APIError(f"Request failed: {str(e)}", 0) from e

        if last_exception:
            raise last_exception

        raise APIError(f"Request failed after {self.max_retries} retries")

    def _handle_error_response(
        self, response: requests.Response, error_data: Optional[Dict[str, Any]]
    ) -> APIError:
        """Handle error responses from the API."""
        status_code = response.status_code
        request_id = ""
        error_code = ""
        message = "An error occurred"
        details = []

        if error_data:
            if "meta" in error_data and "request_id" in error_data["meta"]:
                request_id = error_data["meta"]["request_id"]

            if "error" in error_data:
                error = error_data["error"]
                error_code = error.get("code", "")
                message = error.get("message", "An error occurred")
                details = error.get("details", [])

        if status_code == 401:
            return AuthenticationError(message, status_code, request_id)
        elif status_code == 422:
            return ValidationError(message, details, request_id, status_code)
        elif status_code == 429:
            retry_after = 60
            if "Retry-After" in response.headers:
                try:
                    retry_after = int(response.headers["Retry-After"])
                except ValueError:
                    pass
            return RateLimitError(message, status_code, request_id, retry_after)
        else:
            return APIError(message, status_code, error_code, request_id, details)

    def _is_retryable_error(self, error: Exception) -> bool:
        """Check if an error is retryable."""
        if isinstance(error, requests.exceptions.ConnectionError):
            return True
        if isinstance(error, requests.exceptions.Timeout):
            return True
        return False

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make a GET request."""
        url = f"{self.base_url}{path}"
        request_headers = self._get_default_headers()

        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.get(
                    url=url,
                    params=params,
                    headers=request_headers,
                    timeout=self.timeout,
                )

                if response.status_code == 204:
                    return None

                if response.status_code >= 200 and response.status_code < 300:
                    if response.content:
                        return response.json()
                    return {}

                # Handle errors
                error_data = None
                if response.content:
                    try:
                        error_data = response.json()
                    except ValueError:
                        pass

                api_error = self._handle_error_response(response, error_data)

                # Retry on rate limit
                if isinstance(api_error, RateLimitError) and attempt < self.max_retries:
                    time.sleep(api_error.retry_after)
                    last_exception = api_error
                    continue

                raise api_error

            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < self.max_retries and self._is_retryable_error(e):
                    time.sleep(0.1 * (attempt + 1))  # Exponential backoff
                    continue
                raise APIError(f"Request failed: {str(e)}", 0) from e

        if last_exception:
            raise last_exception

        raise APIError(f"Request failed after {self.max_retries} retries")

    def post(
        self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make a POST request."""
        return self.request("POST", path, data, headers)

    def patch(
        self, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make a PATCH request."""
        return self.request("PATCH", path, data)

    def delete(self, path: str) -> None:
        """Make a DELETE request."""
        self.request("DELETE", path)
