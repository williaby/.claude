# Global Claude Code Configuration

> **Status**: ✅ Active | Production Ready
> **Version**: 1.0.0
> **Last Updated**: 2025-01-16
> **Compatibility**: Claude Code v1.0+

This repository provides universal Claude Code configuration and standards for all development projects, with automated MCP server management.

## Quick Setup

```bash
# Initial setup - clone directly to ~/.claude/
cd ~
git clone https://github.com/williaby/.claude.git .claude

# Set up environment variables and install MCP servers
~/.claude/scripts/setup-env.sh

# Edit the .env file to add your API keys
nano ~/.claude/.env

# Install MCP servers at user level (available globally)
~/.claude/scripts/mcp-manager.sh

# That's it! Claude Code will automatically:
# - Load ~/.claude/CLAUDE.md for global standards
# - Make ~/.claude/commands/ slash commands available
# - Apply global development practices across all projects
# - Use MCP servers you installed across all projects
```

## Directory Structure

```
~/.claude/
├── README.md                     # This file - configuration guide
├── CLAUDE.md                     # Global development standards (auto-loaded)
├── settings.json                 # Claude Code settings (permissions, hooks)
├── .mcp.json                     # MCP server configurations
├── agents/                       # Specialized agent definitions
│   └── *.md                     # Agent capability definitions
├── commands/                     # Universal slash commands
│   ├── quality-*.md             # Code quality and formatting commands
│   ├── security-*.md            # Security validation and checks
│   └── meta-*.md               # Command management utilities
├── context/                      # Shared context files for agents
│   ├── development-standards.md # Quick reference standards
│   ├── integration-patterns.md  # Common integration patterns
│   └── shared-architecture.md   # Architectural guidelines
├── docs/                         # Additional documentation
│   ├── response-aware-development.md  # RAD methodology
│   ├── tdd-enforcement-system.md     # TDD hook documentation
│   └── project-env-loading.md        # Project-specific env guide
├── mcp/                          # MCP server configuration templates
│   └── *.json                   # Server configuration templates
├── scripts/                      # Automation and setup scripts
│   ├── setup-env.sh             # Environment setup
│   ├── mcp-manager.sh           # MCP server installer
│   └── check-mcp-env.sh         # Validation utilities
├── skills/                       # Hierarchical skill definitions
│   ├── git/                     # Git workflow skill
│   ├── quality/                 # Code quality skill
│   ├── rad/                     # Response-Aware Development skill
│   ├── security/                # Security validation skill
│   └── testing/                 # Testing skill
├── standards/                    # Detailed standard specifications
│   ├── python.md                # Python development standards
│   ├── security.md              # Security requirements
│   ├── git-workflow.md          # Git workflow standards
│   └── linting.md               # Linting configuration
├── templates/                    # Project CLAUDE.md templates
│   ├── python-project.md        # Python project template
│   └── general-project.md       # General project template
└── logs/                         # Runtime logs (git-ignored)
```

## Command Categories

### Quality Commands (`quality-*.md`)
**Code formatting and quality validation across file types**

#### `/universal:quality-format-code`
**Purpose**: Format code files according to project standards  
**Usage**: `/universal:quality-format-code src/main.py` or `/universal:quality-format-code *.md`  
**Description**: Detects file type and applies appropriate formatting (Black for Python, markdownlint for Markdown, etc.)

#### `/universal:quality-lint-check`
**Purpose**: Run appropriate linter for any file type  
**Usage**: `/universal:quality-lint-check src/` or `/universal:quality-lint-check README.md`  
**Description**: Automatically detects file types and runs corresponding linters with project-standard configurations

### Security Commands (`security-*.md`)
**Security validation and environment checks**

#### `/universal:security-validate-env`
**Purpose**: Validate security requirements for development environment  
**Usage**: `/universal:security-validate-env`  
**Description**: Checks GPG keys, SSH keys, Git signing configuration, and dependency security

### Git Workflow (Skills)
**Development workflow helpers and validation**

Git workflow functionality is now provided through the **git skill** (`skills/git/`):
- **Branch validation**: Auto-activates on git/branch keywords
- **Commit validation**: Conventional commits checking
- **PR readiness**: Pre-PR validation checks
- **PR preparation**: Automated PR creation with descriptions

### Meta Commands (`meta-*.md`)
**Command management and discovery utilities**

(Future: Add command discovery and help utilities similar to project-level)

## Configuration Levels

### Global Configuration (`~/.claude/CLAUDE.md`)
The `CLAUDE.md` file in this directory provides:
- **Universal development standards** across all projects
- **Security requirements** (GPG/SSH keys, encryption)
- **Code quality standards** (linting, formatting, testing)
- **Git workflow standards** (branch naming, commit messages)
- **Pre-commit linting requirements** for all file types

This file is automatically loaded by Claude Code and applies to all projects.

### Project Configuration (`./CLAUDE.md`)
Each project can have its own `CLAUDE.md` that:
- **Extends** global standards (doesn't replace them)
- **Adds project-specific** requirements and patterns
- **Defines unique** development workflows
- **Specifies project** architecture and context

### Local Settings (`settings.json`)
User preferences and MCP server configurations:
```json
{
  "command_defaults": {
    "quality_preference": "strict",
    "security_level": "high",
    "workflow_mode": "standard"
  },
  "mcpServers": {
    // MCP server configurations
  }
}
```

## MCP Server Management

### Available MCP Servers
**Current Working Servers**:
- **Core**: zen (orchestration server)
- **Development**: git, sequential-thinking, time, github
- **Search**: tavily (web search), context7-sse (SSE transport)
- **Automation**: zapier (HTTP-based workflows)
- **Project-Level**: serena (advanced NLP, project-specific)

### Installation
```bash
# Interactive installer for user-level MCP servers
~/.claude/scripts/mcp-manager.sh

# Install project-specific MCP servers
~/.claude/scripts/setup-project-mcp.sh

# Validate environment variables and API keys
~/.claude/scripts/check-mcp-env.sh
```

### Project-Specific MCP Servers
For MCP servers that need project-specific paths (like Serena), create a `.mcp.json` in your project:

```json
{
  "mcpServers": {
    "serena": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/your-username/dev/serena",
        "serena-mcp-server",
        "--context",
        "ide-assistant",
        "--project",
        "."
      ]
    }
  }
}
```

## Command Development Standards

### Naming Convention
```
{category}-{action}-{object}.md
```
**Examples**:
- `quality-format-code.md`
- `security-validate-env.md`
- `workflow-git-helpers.md`

### Categories
- **quality**: Code formatting and linting (< 5 min)
- **security**: Security validation and checks (< 5 min)
- **workflow**: Development workflow helpers (5-15 min)
- **meta**: Command management utilities (< 5 min)

### Command Structure Template
```markdown
---
category: quality|security|workflow|meta
complexity: low|medium|high
estimated_time: "5-15 minutes"
dependencies: []
version: "1.0"
---

# {Category} {Action} {Object}

Brief description of command purpose: $ARGUMENTS

## Usage Options
[Specific usage patterns]

## Instructions
[Detailed command logic]

## Error Handling
[Recovery strategies]

## Examples
[Usage examples]
```

## Security Best Practices

### Required Security Components
1. **GPG Key**: For .env file encryption/decryption
2. **SSH Key**: For signed commits to GitHub
3. **Git Signing**: Properly configured commit signing
4. **Dependency Scanning**: Regular vulnerability checks

### Validation Command
```bash
/universal:security-validate-env
```

This command checks all security requirements and provides setup instructions for any missing components.

## Updates and Maintenance

### Getting Updates
```bash
# Update global standards and commands
cd ~/.claude
git pull

# Re-run setup if new MCP servers are added
~/.claude/scripts/mcp-manager.sh
```

### Version History
Check [CHANGELOG.md](CHANGELOG.md) for:
- New features and commands
- Breaking changes
- Bug fixes
- MCP server updates

## Benefits

- **Universal Standards**: Consistent development practices across all projects
- **Automatic Loading**: Claude Code automatically applies global configuration
- **Command Discovery**: Easy-to-find commands with clear categorization
- **Security First**: Built-in security validation and best practices
- **MCP Integration**: Centralized management of AI model integrations
- **Team Consistency**: Shared standards for all team members

## Troubleshooting

### Common Issues
- **Commands not found**: Ensure ~/.claude/commands/ exists
- **MCP servers not working**: Run `~/.claude/scripts/check-mcp-env.sh`
- **Security validation fails**: Follow setup instructions from validation command
- **Settings not applied**: Check that CLAUDE.md is properly formatted

### Debug Commands
```bash
# Check MCP server status
~/.claude/scripts/check-mcp-env.sh

# Validate environment setup
/universal:security-validate-env

# Test command loading
ls ~/.claude/commands/
```

## Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/new-command`
3. Add your command following naming conventions
4. Test across multiple projects
5. Submit a pull request with clear description

## Resources

### Claude Code Documentation
- [Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Memory Management](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### MCP Server Documentation
- Individual server docs in `mcp/` directory
- API key requirements in `.env.example`
- Project-specific setup in `docs/project-env-loading.md`

---

*This configuration is automatically loaded by Claude Code. For project-specific instructions, see the project's CLAUDE.md file.*