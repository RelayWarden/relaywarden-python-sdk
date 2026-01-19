# Contributing to RelayWarden Python SDK

Thank you for your interest in contributing to the RelayWarden Python SDK! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip
- Git

### Setting Up the Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/relaywarden-python-sdk.git
   cd relaywarden-python-sdk
   ```
3. Install the package with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Making Changes

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Ensure code follows PEP 8 style guidelines
4. Write or update tests
5. Run type checking:
   ```bash
   mypy relaywarden
   ```
6. Format code:
   ```bash
   black relaywarden tests
   ```
7. Run tests:
   ```bash
   pytest
   pytest --cov=relaywarden
   ```
8. Commit your changes with clear, descriptive messages

### Coding Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use type hints for function parameters and return types
- Add docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable and function names

### Type Hints

- Use type hints for all function parameters and return values
- Use `typing` module for complex types
- Run `mypy` to check type correctness
- Add type hints even if not strictly required

### Testing

- Write tests for all new functionality
- Use pytest for testing
- Ensure all tests pass before submitting
- Aim for high test coverage
- Test both success and error cases
- Use fixtures for common test data

### Code Formatting

- Use [Black](https://black.readthedocs.io/) for code formatting
- Line length: 100 characters
- Run `black` before committing

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(messages): add support for message cancellation

Add the ability to cancel pending messages via the API.
This includes retry logic and proper error handling.
```

## Submitting Changes

1. Push your branch to your fork
2. Create a Pull Request targeting the `main` branch
3. Fill out the PR template completely
4. Ensure all CI checks pass
5. Address any review feedback

### Pull Request Checklist

- [ ] Code follows PEP 8 standards
- [ ] Type checking passes (mypy)
- [ ] Code formatted with black
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Commit messages follow Conventional Commits
- [ ] PR description is clear and complete

## Reporting Issues

When reporting bugs or requesting features:

1. Check existing issues to avoid duplicates
2. Use the appropriate issue template
3. Provide clear steps to reproduce (for bugs)
4. Include Python version, SDK version, and environment details
5. Add code examples when relevant

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new public APIs
- Keep code examples up to date
- Follow Google or NumPy docstring style

## Questions?

- Open a discussion for questions
- Check existing issues and discussions
- Review the README for common usage patterns

Thank you for contributing! 🎉
