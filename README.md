# RelayWarden Python SDK

Official Python SDK for the RelayWarden API v1.

## Installation

```bash
pip install relaywarden
```

Or from source:

```bash
pip install -e .
```

## Quick Start

```python
from relaywarden import Client

# Initialize the client
client = Client(
    base_url="https://api.relaywarden.eu/api/v1",
    token="your-api-token"
)

# Set project ID for project-scoped operations
client.set_project_id("your-project-id")

# Send a message
message = client.messages.send({
    "from": {
        "email": "noreply@example.com",
        "name": "Acme Corp"
    },
    "to": [
        {"email": "user@example.com"}
    ],
    "subject": "Welcome!",
    "html": "<h1>Welcome!</h1>",
    "text": "Welcome!"
}, idempotency_key="unique-key-123")

print(f"Message ID: {message['data']['message_id']}")
```

## Authentication

The SDK uses Bearer token authentication. Pass your API token when creating the client:

```python
client = Client(
    base_url="https://api.relaywarden.eu/api/v1",
    token="your-api-token"
)
```

## Resources

### Identity

```python
# Get current user/service account info
me = client.identity.me()

# List teams
teams = client.identity.teams()
```

### Projects

```python
# List projects
projects = client.projects.list({"environment": "production"})

# Create project
project = client.projects.create({
    "name": "Production",
    "environment": "production"
})

# Get project
project = client.projects.get("project-id")

# Update project
project = client.projects.update("project-id", {
    "name": "Updated Name"
})

# Delete project
client.projects.delete("project-id")
```

### Messages

```python
# Send message with idempotency key
message = client.messages.send({
    "from": {"email": "noreply@example.com"},
    "to": [{"email": "user@example.com"}],
    "subject": "Hello",
    "html": "<h1>Hello</h1>"
}, idempotency_key="unique-key-123")

# List messages
messages = client.messages.list({
    "status": "delivered",
    "per_page": 25
})

# Get message
message = client.messages.get("message-id")

# Get message timeline
timeline = client.messages.get_timeline("message-id")

# Cancel message
client.messages.cancel("message-id")

# Resend message
client.messages.resend("message-id")
```

### Templates

```python
# Create template
template = client.templates.create({
    "name": "Welcome Email",
    "subject": "Welcome {{ $name }}!",
    "html_body": "<h1>Welcome {{ $name }}!</h1>",
    "text_body": "Welcome {{ $name }}!"
})

# Render template
rendered = client.templates.render("template-id", {
    "data": {"name": "John"}
})

# Test send
client.templates.test_send("template-id", {
    "to": "test@example.com",
    "data": {"name": "John"}
})
```

### Domains

```python
# Create domain
domain = client.domains.create({
    "domain": "mail.example.com"
})

# Verify domain
result = client.domains.verify("domain-id")

# Get DNS records
records = client.domains.get_dns_records("domain-id")

# Rotate DKIM keys
client.domains.rotate_dkim("domain-id")
```

## Error Handling

The SDK raises specific exception types for different error scenarios:

```python
from relaywarden.exceptions import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError
)

try:
    message = client.messages.send({...})
except AuthenticationError as e:
    # 401 - Invalid or missing token
    print(f"Authentication failed: {e.message}")
except ValidationError as e:
    # 422 - Validation errors
    print(f"Validation failed: {e.message}")
    for detail in e.details:
        print(f"  {detail['field']}: {detail['message']}")
except RateLimitError as e:
    # 429 - Rate limit exceeded
    print(f"Rate limit exceeded. Retry after: {e.retry_after} seconds")
except APIError as e:
    # Other API errors
    print(f"API Error: {e.message} [Request ID: {e.request_id}]")
```

## Pagination

List endpoints return paginated responses:

```python
response = client.messages.list()

# Access pagination metadata
current_page = response['meta']['current_page']
total = response['meta']['total']
last_page = response['meta']['last_page']

# Access data
messages = response['data']
```

## Rate Limiting

The SDK automatically handles rate limits with exponential backoff. Rate limit information is available in the exception:

```python
try:
    client.messages.send({...})
except RateLimitError as e:
    retry_after = e.retry_after  # Seconds to wait
    # SDK will automatically retry, but you can also handle manually
```

## Configuration

```python
client = Client(
    base_url="https://api.relaywarden.eu/api/v1",
    token="your-token",
    max_retries=3,
    timeout=30
)
```

## Testing

```bash
pytest
pytest --cov=relaywarden
```

## License

MIT
