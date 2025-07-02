# Global Claude Code Configuration

This repository provides universal Claude Code configuration and standards for all development projects.

## Quick Setup

```bash
# Initial setup - clone directly to ~/.claude/
cd ~
git clone https://github.com/your-username/.claude.git

# Set up environment variables for MCP servers
~/.claude/scripts/setup-env.sh

# Edit the .env file to add your API keys
nano ~/.claude/.env

# That's it! Claude Code will automatically:
# - Load ~/.claude/CLAUDE.md for global standards
# - Make ~/.claude/commands/ slash commands available
# - Apply global development practices across all projects
# - Use your API keys for MCP server configurations
```

## What's Included

### Global Standards (`CLAUDE.md`)
- Universal development commands (formatting, linting, testing)
- Security validation requirements (GPG/SSH keys)
- Code quality standards (Python, Markdown, YAML, JSON)
- Git workflow patterns (branch naming, commit messages)
- Pre-commit checklist and best practices

### Universal Slash Commands (`commands/`)
- `/universal:lint-check` - Run appropriate linter for any file type
- `/universal:security-validate` - Validate GPG/SSH keys and security setup
- `/universal:format-code` - Format code according to project standards
- `/universal:git-workflow` - Git workflow helpers and validation

### Template Configurations (`settings/`, `mcp/`)
- Base settings templates for common tool permissions
- Common MCP server configurations:
  - **Search & Information**: perplexity, tavily
  - **Development tools**: github, git, sequential-thinking, time
  - **Infrastructure**: context7 (Redis), sentry (monitoring)
  - **Automation**: zapier (workflow automation)
  - **AI Assistants**: serena (development assistant)
- Environment variable templates for secure API key storage
- Example configurations for new projects

## Updates

```bash
# Get latest global standards
cd ~/.claude
git pull
```

## Project Integration

Your project's `CLAUDE.md` should focus on project-specific information while the global standards are automatically applied:

```markdown
# My Project Claude Configuration

## Project Overview
[Your project-specific architecture and context]

## Domain-Specific Standards  
[Any project-specific conventions and requirements]

## Development Workflows
[Project-specific development processes]
```

## File Structure

```
~/.claude/
├── CLAUDE.md                     # Global standards (auto-loaded)
├── commands/                     # Universal slash commands (auto-loaded)
│   ├── lint-check.md
│   ├── security-validate.md
│   ├── format-code.md
│   └── git-workflow.md
├── settings/
│   ├── base-settings.json        # Template settings
│   └── base-permissions.json     # Common permissions
├── mcp/
│   └── common-servers.json       # Common MCP servers
├── scripts/
│   ├── setup-env.sh              # Environment setup script
│   └── update.sh                 # Update helper script
└── .env.example                  # Template for API keys (DO NOT COMMIT .env!)
```

## Benefits

- **No Duplication**: Universal standards shared across all projects
- **Automatic Loading**: Leverages Claude Code's built-in global support
- **Version Controlled**: Global standards are versioned and updatable
- **Simple Setup**: One `git clone` command sets up everything
- **Team Consistency**: Shared standards across all team members

## Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/improve-standards`
3. Make your changes to global standards
4. Test with multiple projects to ensure compatibility
5. Submit a pull request with clear description of changes

## Versioning

This repository uses semantic versioning:
- **Major** (1.0.0): Breaking changes to global standards
- **Minor** (1.1.0): New features or non-breaking improvements
- **Patch** (1.1.1): Bug fixes and minor corrections

Check the [CHANGELOG.md](CHANGELOG.md) for version history and upgrade notes.