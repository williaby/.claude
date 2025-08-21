# AI Tools Slash Command Documentation

## Overview

The `/tools:ai-validate` slash command provides universal AI coding tools validation and setup across all development projects. This user-level command is available in any Claude Code session and automatically adapts to different project types.

## Installation

The command is now installed in your user-level Claude configuration:

```
~/.claude/
├── commands/
│   └── tools-ai-validate.md          # Slash command definition
└── scripts/
    ├── ai_tools_validator.py          # Main validation logic
    └── tools_ai_validate_launcher.py  # Command launcher
```

## Usage

### Basic Commands

```bash
# Full validation report
/tools:ai-validate

# Quick status check
/tools:ai-validate --quiet

# Setup project configuration
/tools:ai-validate --setup

# Attempt installation of missing tools
/tools:ai-validate --install
```

### Sample Output

#### Full Report
```
🤖 AI Coding Tools Validation Report - PromptCraft
============================================================
Project Type: Python
Languages: python, javascript

⚠️ Claude Code (v1.0.84)
   Missing env vars: ANTHROPIC_API_KEY

❌ GitHub Copilot CLI - Not installed
   Install GitHub Copilot CLI:
   1. Install GitHub CLI: https://cli.github.com/
   2. Run: gh extension install github/gh-copilot
   3. Login: gh auth login
   4. Verify with: gh copilot --version

✅ OpenAI Codex CLI (v1.10.0)
```

#### Quiet Mode
```
AI Tools: 3/5 installed, 2/5 configured
```

## Supported Tools

| Tool | Detection | Auto-Install | Configuration |
|------|-----------|--------------|---------------|
| **Claude Code** | `claude --version` | Manual | `.claude/settings.json` |
| **GitHub Copilot CLI** | `gh copilot --version` | `gh extension install` | `.github/copilot.yml` |
| **Gemini CLI** | `gemini --version` | Manual | `.gemini/config.json` |
| **Qwen Code CLI** | `qwen --version` | Manual | `.qwen/config.json` |
| **OpenAI CLI** | `openai --version` | `pip install openai[cli]` | `.openai/config.json` |

## Project Type Detection

The command automatically detects project characteristics:

### Python Projects
- **Detection**: `pyproject.toml`, `setup.py`, `requirements.txt`
- **Package Managers**: Poetry, pip
- **Frameworks**: FastAPI, Django, Flask, Gradio
- **Config Focus**: Python-specific linting, formatting, testing

### JavaScript/Node.js Projects
- **Detection**: `package.json`, `yarn.lock`
- **Package Managers**: npm, yarn, pnpm
- **Frameworks**: React, Vue, Express, Next.js
- **Config Focus**: ESLint, Prettier, TypeScript support

### Rust Projects
- **Detection**: `Cargo.toml`
- **Package Manager**: Cargo
- **Config Focus**: Rust toolchain, clippy, rustfmt

### Go Projects
- **Detection**: `go.mod`, `go.sum`
- **Package Manager**: go modules
- **Config Focus**: gofmt, golint, go tools

### Generic Projects
- **Detection**: Git repository without specific language markers
- **Config Focus**: Basic AI tool setup with common exclusions

## Configuration Templates

### Project-Specific Configurations

Each tool receives project-appropriate configuration:

#### Claude Code (`.claude/settings.json`)
```json
{
  "project": {
    "name": "project-name",
    "type": "python",
    "languages": ["python", "javascript"]
  },
  "tools": {
    "enabled": ["basic_commands"],
    "disabled": []
  }
}
```

#### GitHub Copilot (`.github/copilot.yml`)
```yaml
suggestions:
  enabled: true
  languages:
    python: true
    javascript: true
    typescript: true

exclude:
  - "*.env*"
  - "**/node_modules/**"
  - "**/.venv/**"
  - "**/__pycache__/**"
```

#### Gemini CLI (`.gemini/config.json`)
```json
{
  "project": "project-name",
  "settings": {
    "model": "gemini-2.0-flash-exp",
    "temperature": 0.3,
    "max_tokens": 4096
  },
  "project_context": {
    "type": "python",
    "languages": ["python", "javascript"],
    "frameworks": ["fastapi", "gradio"]
  },
  "exclusions": {
    "files": ["*.env*", "*.log"],
    "directories": [".mypy_cache", ".pytest_cache", "build"]
  }
}
```

## VS Code Integration

When a `.vscode/` directory exists, the command automatically:

### Updates Settings (`.vscode/settings.json`)
```json
{
  "ai-tools": {
    "validation": {
      "enabled": true,
      "checkOnOpen": true,
      "createTemplates": true,
      "tools": ["claude", "copilot", "gemini", "qwen", "codex"]
    }
  }
}
```

### Adds Validation Task (`.vscode/tasks.json`)
```json
{
  "label": "Validate AI Tools",
  "type": "shell",
  "command": "python",
  "args": ["~/.claude/scripts/ai_tools_validator.py", "--setup-project"],
  "runOptions": {
    "runOn": "folderOpen"
  }
}
```

## Environment Variables

The command checks for required API keys:

```bash
# Create .env file in your project or set globally
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_AI_API_KEY=your_gemini_api_key
GEMINI_API_KEY=your_gemini_api_key_alternative
QWEN_API_KEY=your_qwen_api_key
GITHUB_TOKEN=your_github_token
```

## Command Implementation

The slash command works through a three-layer architecture:

1. **Command Definition** (`tools-ai-validate.md`): Claude Code command specification
2. **Launcher** (`tools_ai_validate_launcher.py`): Argument processing and execution
3. **Validator** (`ai_tools_validator.py`): Core validation and setup logic

### Command Flow
```
/tools:ai-validate --setup
    ↓
tools_ai_validate_launcher.py
    ↓ (--setup-project)
ai_tools_validator.py
    ↓
[Project Detection] → [Tool Validation] → [Config Generation] → [VS Code Setup]
```

## Exit Codes

- `0`: All tools installed and configured
- `1`: Some tools installed but not fully configured
- `2`: No AI tools installed

## Integration Examples

### Daily Development Workflow

```bash
# New project setup
cd /path/to/new/project
/tools:ai-validate --setup

# Quick morning check
/tools:ai-validate --quiet

# After installing new tools
/tools:ai-validate --install
```

### CI/CD Pipeline Integration

```bash
#!/bin/bash
# In your CI script
if /tools:ai-validate --quiet | grep -q "5/5 configured"; then
  echo "✅ All AI tools ready"
else
  echo "⚠️ AI tools setup incomplete"
  /tools:ai-validate  # Show full report
fi
```

### Project Onboarding Scripts

```bash
#!/bin/bash
# project-setup.sh
echo "Setting up development environment..."
/tools:ai-validate --setup --install
echo "AI tools configuration complete!"
```

## Troubleshooting

### Common Issues

#### Tool Not Detected
```bash
# Check if tool is in PATH
which claude
which gh
which openai

# Verify installation
claude --version
gh copilot --version
openai --version
```

#### Configuration Issues
```bash
# Re-create templates
/tools:ai-validate --setup

# Check environment variables
env | grep -E "(ANTHROPIC|OPENAI|GEMINI|QWEN|GITHUB)"

# Validate JSON/YAML syntax
python -m json.tool .claude/settings.json
python -m yaml tool check .github/copilot.yml
```

#### VS Code Integration Problems
```bash
# Check VS Code configuration
cat .vscode/settings.json
cat .vscode/tasks.json

# Re-run setup
/tools:ai-validate --setup

# Restart VS Code
code . --disable-extensions  # Test without extensions
```

### Debug Mode

```bash
# Run with Python directly for debugging
python ~/.claude/scripts/ai_tools_validator.py --setup-project

# Check script permissions
ls -la ~/.claude/scripts/
```

## Advanced Usage

### Custom Project Types

You can extend the validator for custom project types by modifying the `_detect_project_type` method in `ai_tools_validator.py`.

### Tool-Specific Configuration

Each tool's configuration can be customized after initial setup:

```bash
# Edit configurations after setup
code .claude/settings.json
code .github/copilot.yml
code .gemini/config.json
```

### Selective Tool Validation

The validator can be extended to support selective tool checking:

```python
# Future enhancement - selective validation
/tools:ai-validate --tools=claude,copilot
```

## Related Commands

- `/security:validate-env` - Environment and secrets validation
- `/quality:precommit-validate` - Pre-commit hooks validation
- `/workflow:git-helpers` - Git workflow assistance

---

**Command Status**: ✅ Ready for use  
**Compatibility**: All Claude Code installations  
**Last Updated**: 2025-08-19