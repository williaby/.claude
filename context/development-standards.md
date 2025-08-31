# Universal Development Standards

## Code Quality Standards

### Formatting & Linting

```bash
# Format and lint commands
poetry run black .                    # 88-character line length
poetry run ruff check --fix .         # Comprehensive linting
poetry run mypy src                    # Type checking
markdownlint **/*.md                  # Markdown formatting
yamllint **/*.{yml,yaml}              # YAML validation
```

### Security Validation

```bash
# Required security checks
gpg --list-secret-keys                # GPG key validation
ssh-add -l                           # SSH key validation
git config --get user.signingkey     # Git signing configuration
poetry run safety check              # Dependency vulnerability scanning
poetry run bandit -r src             # Security static analysis
```

### Testing Standards

```bash
# Testing commands by tier
poetry run pytest tests/unit/ --maxfail=3 -n auto                    # Fast feedback
poetry run pytest tests/unit/ tests/integration/ --cov=src --cov-fail-under=80  # Pre-commit
poetry run pytest --cov=src --cov-report=html --cov-report=term-missing         # Full suite
```

## Naming Conventions

### File Naming

- **Python**: snake_case.py (e.g., user_service.py, query_counselor.py)
- **Test Files**: test_*.py (e.g., test_user_service.py)
- **Configuration**: lowercase with hyphens (e.g., docker-compose.yml)
- **Documentation**: lowercase with hyphens (e.g., api-reference.md)

### Code Naming

- **Functions/Variables**: snake_case (e.g., process_user_data, user_id)
- **Classes**: PascalCase (e.g., UserService, QueryCounselor)
- **Constants**: UPPER_SNAKE_CASE (e.g., MAX_RETRY_COUNT, API_BASE_URL)
- **Private Methods**: _leading_underscore (e.g., _validate_input)

## Documentation Standards

### Code Documentation

```python
def process_user_data(user_data: dict) -> User:
    """
    Process and validate user registration data.
    
    Args:
        user_data: Dictionary containing user information with required
                  fields: email, password, name
    
    Returns:
        User: Created user object with generated ID and timestamps
    
    Raises:
        ValidationError: When user_data is invalid or incomplete
        DuplicateEmailError: When email already exists
    """
```

### Markdown Standards

- Use sentence case for headings
- 120-character line length maximum
- Include table of contents for documents > 100 lines
- Use code blocks with language specification
- Include examples for complex concepts

### Git Standards

- Conventional commits (feat:, fix:, docs:, test:, refactor:)
- All commits must be signed (GPG key required)
- Branch naming: feature/description, fix/description, docs/description
- Pull requests require review and passing CI

## Environment Standards

### Required Environment Setup

- Python 3.11+ with Poetry installed
- GPG key configured for secret encryption
- SSH key configured for Git signing
- Pre-commit hooks installed and active

### Security Requirements

- All .env files must be encrypted with GPG
- No secrets in code or configuration files
- Service accounts stored securely (.gcp/service-account.json)
- Regular dependency vulnerability scanning

### Development Workflow

1. Create feature branch from main
2. Implement changes following standards
3. Run quality checks (format, lint, test)
4. Create signed commit with conventional format
5. Push branch and create pull request
6. Review, approve, and merge with signed merge commit
