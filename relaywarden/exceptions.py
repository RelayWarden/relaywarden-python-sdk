"""Exception classes for the RelayWarden SDK."""


class APIError(Exception):
    """Base exception for all API errors."""

    def __init__(
        self,
        message: str,
        code: int = 0,
        error_code: str = "",
        request_id: str = "",
        details: list = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.error_code = error_code
        self.request_id = request_id
        self.details = details or []

    def __str__(self) -> str:
        return f"API error ({self.code}): {self.message} [Request ID: {self.request_id}]"


class AuthenticationError(APIError):
    """Exception raised when authentication fails."""

    def __init__(self, message: str, code: int = 401, request_id: str = ""):
        super().__init__(message, code, "unauthorized", request_id)
        self.message = message
        self.code = code
        self.request_id = request_id

    def __str__(self) -> str:
        return f"Authentication failed: {self.message} [Request ID: {self.request_id}]"


class RateLimitError(APIError):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, message: str, code: int = 429, request_id: str = "", retry_after: int = 60):
        super().__init__(message, code, "rate_limit_exceeded", request_id)
        self.message = message
        self.code = code
        self.request_id = request_id
        self.retry_after = retry_after

    def __str__(self) -> str:
        return (
            f"Rate limit exceeded: {self.message} "
            f"[Retry after: {self.retry_after} seconds, Request ID: {self.request_id}]"
        )


class ValidationError(APIError):
    """Exception raised when request validation fails."""

    def __init__(self, message: str, details: list = None, request_id: str = "", code: int = 422):
        super().__init__(message, code, "validation_error", request_id, details)
        self.message = message
        self.details = details or []
        self.request_id = request_id
        self.code = code

    def __str__(self) -> str:
        return f"Validation failed: {self.message} [Request ID: {self.request_id}]"
