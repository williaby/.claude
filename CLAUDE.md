# Global Claude Development Standards

This file provides universal development standards and practices for Claude Code across all projects.

## Universal Development Commands

### Code Quality and Formatting
```bash
# Format code (Python projects)
poetry run black .
poetry run ruff check --fix .

# Run linting checks (Python projects)
poetry run black --check .
poetry run ruff check .
poetry run mypy src

# Markdown linting (MANDATORY for all .md files)
markdownlint **/*.md

# YAML linting (MANDATORY for all .yml/.yaml files)
yamllint **/*.{yml,yaml}

# Run all pre-commit hooks manually
poetry run pre-commit run --all-files
```

### Security Validation
```bash
# REQUIRED: Validate GPG and SSH keys are present
gpg --list-secret-keys  # Must show GPG key for .env encryption
ssh-add -l              # Must show SSH key for signed commits
git config --get user.signingkey  # Must be configured for signed commits

# Run security scans (Python projects)
poetry run safety check
poetry run bandit -r src
```

### Testing Standards
```bash
# Run all tests with coverage (Python projects)
poetry run pytest -v --cov=src --cov-report=html --cov-report=term-missing

# Minimum 80% test coverage required for all Python code
```

## Universal Development Standards

### Code Quality Requirements
- **Python**: Black formatting (88 char line length), Ruff linting, MyPy type checking
- **Markdown**: 120 character line length, consistent list styles, proper heading hierarchy
- **YAML**: 2-space indentation, 120 character line length
- **Test Coverage**: Minimum 80% for all Python code
- **Pre-commit Hooks**: Mandatory for all projects

### Security Requirements
- **GPG Key**: MUST be present for .env encryption/decryption
- **SSH Key**: MUST be present for signed commits to GitHub
- **Key Validation**: Environment MUST validate both GPG and SSH keys are available
- **Dependency Security**: All projects must use Safety and Bandit for security scanning
- **Secrets Management**: Use local encrypted .env files (no secrets in code or commits)

### Git Workflow Standards
- **Branch Naming**: feature/<issue-number>-<short-name>, fix/<issue-number>-<short-name>
- **Commit Messages**: Follow Conventional Commits format
- **PR Requirements**: Must link to GitHub issue (e.g., "Closes #21")
- **PR Size**: Keep PRs under 400 lines when possible
- **Commit Signing**: All commits must be signed

### File-Type Specific Linting (MANDATORY COMPLIANCE)
**ALL modifications to files MUST comply with these linting standards:**

#### Markdown Files (.md)
- **Command**: `markdownlint **/*.md`
- **Requirements**: 120 character line length, consistent list styles, proper heading hierarchy
- **MUST RUN** before committing any markdown changes

#### YAML Files (.yml, .yaml)
- **Command**: `yamllint **/*.{yml,yaml}`
- **Requirements**: 2-space indentation, 120 character line length
- **MUST RUN** before committing any YAML changes

#### Python Files (.py)
- **Commands**: `black --check .`, `ruff check .`, `mypy src`
- **Requirements**: 88 character line length, comprehensive rule compliance
- **MUST RUN** before committing any Python changes

#### JSON Files (.json)
- **Validation**: Automatic via pre-commit hooks
- **Requirements**: Valid JSON syntax, proper formatting

## Pre-Commit Linting Checklist
Before committing ANY changes, ensure:
- [ ] Environment validation passes (GPG and SSH keys present)
- [ ] File-specific linter has been run and passes
- [ ] Pre-commit hooks execute successfully
- [ ] No linting warnings or errors remain
- [ ] Code formatting is consistent with project standards
- [ ] Commits are signed (Git signing key configured)

## Development Philosophy
1. **Security First**: Always validate keys, encrypt secrets, scan dependencies
2. **Quality Standards**: Maintain consistent code quality across all projects
3. **Documentation**: Keep documentation current and well-formatted
4. **Testing**: Maintain high test coverage and run tests before commits
5. **Collaboration**: Use consistent Git workflows and clear commit messages

---

*This configuration is automatically loaded by Claude Code. For project-specific instructions, see the project's CLAUDE.md file.*