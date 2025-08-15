# Global Claude Development Standards

> Universal development standards and practices for Claude Code across all projects.
>
> **Token Optimized**: This streamlined file references detailed specifications in `/standards/` 
> and `/commands/` directories for maximum efficiency while maintaining comprehensive coverage.

## Core Development Standards

> **Detailed Specifications**: See `/standards/python.md`, `/standards/security.md`, `/standards/git-workflow.md`, `/standards/linting.md`

### Essential Requirements
- **Code Quality**: Black formatting (88 chars), Ruff linting, MyPy type checking
- **Security**: GPG/SSH key validation, dependency scanning, encrypted secrets
- **Testing**: Minimum 80% coverage, tiered testing approach
- **Git**: Conventional commits, signed commits, feature branch workflow

### File-Type Standards
- **Python**: 88-char line length, comprehensive rule compliance
- **Markdown**: 120-char line length, consistent formatting  
- **YAML**: 2-space indentation, 120-char line length
- **Validation**: Pre-commit hooks enforce all standards

## Essential Commands

> **Complete Command Reference**: See `/commands/quality.md`, `/commands/testing.md`, `/commands/security.md`

### Code Quality & Formatting
```bash
# Format and lint (see /commands/quality.md for full details)
poetry run black .
poetry run ruff check --fix .
poetry run mypy src
markdownlint **/*.md
yamllint **/*.{yml,yaml}
```

### Security Validation
```bash
# Key validation (see /commands/security.md for full details)
gpg --list-secret-keys  # Must show GPG key for .env encryption
ssh-add -l              # Must show SSH key for signed commits
git config --get user.signingkey  # Must be configured for signed commits
poetry run safety check
poetry run bandit -r src
```

### Testing Standards
```bash
# Testing commands (see /commands/testing.md for full details)
poetry run pytest -v --cov=src --cov-report=html --cov-report=term-missing
poetry run pre-commit run --all-files
```

## Project Integration

> **Project Templates**: Use `/templates/python-project.md` or `/templates/general-project.md` for new projects

### Implementation Pattern
Projects create focused `CLAUDE.md` files that **extend** (not duplicate) these global standards:

1. **Reference Pattern**: Use `> Reference: /standards/[domain].md` for detailed requirements
2. **Project Focus**: Include only project-specific configurations and deviations
3. **Inheritance**: All universal standards automatically apply unless overridden

### Example Project Structure
```markdown
# Project Development Guide

> This project extends the global CLAUDE.md standards. Only project-specific 
> configurations and deviations are documented below.

## Project-Specific Standards
> Reference: Global standards apply. Project-specific requirements below.

- **Performance**: API response p95 < 2s
- **Security**: Service account at `.gcp/service-account.json`
- **Architecture**: External Qdrant at 192.168.1.16:6333
```

## Development Philosophy

**Security First** → **Quality Standards** → **Documentation** → **Testing** → **Collaboration**

### Core Principles
1. **Security First**: Always validate keys, encrypt secrets, scan dependencies
2. **Quality Standards**: Maintain consistent code quality across all projects  
3. **Documentation**: Keep documentation current and well-formatted
4. **Testing**: Maintain high test coverage and run tests before commits
5. **Collaboration**: Use consistent Git workflows and clear commit messages

## Pre-Commit Linting Checklist

Before committing ANY changes, ensure:
- [ ] Environment validation passes (GPG and SSH keys present)
- [ ] File-specific linter has been run and passes
- [ ] Pre-commit hooks execute successfully
- [ ] No linting warnings or errors remain
- [ ] Code formatting is consistent with project standards
- [ ] Commits are signed (Git signing key configured)

---

*This modular configuration is automatically loaded by Claude Code. For detailed specifications, see referenced files in `/standards/` and `/commands/` directories.*

*Modularization complete! All detailed specifications are now available in domain-specific files for maximum token efficiency.*