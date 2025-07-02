# Changelog

All notable changes to the global Claude Code configuration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-02

### Added
- Initial global Claude Code configuration structure
- Universal development standards in `CLAUDE.md`
- Universal slash commands:
  - `/universal:lint-check` - File type detection and appropriate linting
  - `/universal:security-validate` - Security setup validation (GPG/SSH keys)
  - `/universal:format-code` - Code formatting for multiple file types
  - `/universal:git-workflow` - Git workflow helpers and validation
- Base settings template with common tool permissions
- Common MCP server configurations (perplexity, tavily, context7, sentry)
- Automated update script (`scripts/update.sh`)
- Comprehensive documentation and setup instructions

### Security
- GPG key validation for .env encryption requirements
- SSH key validation for signed commit requirements
- Security scanning integration (Safety, Bandit)
- Git workflow security checks

### Documentation
- Complete README with setup and usage instructions
- Individual command documentation with examples
- Best practices and development standards
- Migration guide from project-specific configurations

## Standards Included

### Code Quality
- Python: Black (88 chars), Ruff linting, MyPy type checking
- Markdown: 120 char line length, consistent formatting
- YAML: 2-space indentation, 120 char line length
- JSON: Automatic formatting and validation

### Security Requirements
- GPG keys for encryption/decryption
- SSH keys for signed commits
- Dependency vulnerability scanning
- Pre-commit security validation

### Git Workflow
- Conventional Commits format
- Branch naming conventions (feature/fix/hotfix + issue numbers)
- PR size guidelines (< 400 lines)
- Automated workflow validation

### Testing Standards
- Minimum 80% test coverage for Python projects
- Pre-commit hook enforcement
- Security scanning integration