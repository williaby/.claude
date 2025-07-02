# MCP Server Configuration

This directory contains Model Context Protocol (MCP) server configurations for Claude Code's global setup.

## Overview

Each JSON file defines one or more MCP servers that provide specialized capabilities to Claude Code. When `enableAllProjectMcpServers: true` is set in `settings/base-settings.json`, all configurations in this directory should be loaded automatically.

## Configuration Files

### Core Servers
- `zen-server.json` - Central orchestration server (⚠️ **MISSING FROM GIT**)
- `dev-tools-servers.json` - Development utilities (sequential-thinking, git, time)
- `github-server.json` - GitHub API integration

### Search & AI Servers  
- `common-servers.json` - External APIs (perplexity, tavily, context7, sentry)
- `context7-http.json` / `context7-sse.json` - Context7 transport variants

### Specialized Servers
- `serena-server.json` - Advanced NLP capabilities
- `serena-auto-server.json` - Automated Serena configuration
- `zapier-server.json` - Workflow automation

## Required Environment Variables

Many MCP servers require environment variables to function. Ensure these are set in your shell or `.env` files:

### Development Tools
```bash
export GIT_REPO_PATH="/path/to/default/repository"
```

### GitHub Integration
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_xxxxxxxxxxxx"
```

### Serena NLP
```bash
export SERENA_INSTALL_PATH="/path/to/serena-mcp-server"
export SERENA_PROJECT_PATH="/path/to/current/project"
```

### External APIs
```bash
export PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxx"
export TAVILY_API_KEY="tvly-xxxxxxxxxxxx"
export UPSTASH_REDIS_REST_URL="https://xxxxx.upstash.io"
export UPSTASH_REDIS_REST_TOKEN="xxxxxxxxxxxx"
export SENTRY_AUTH_TOKEN="xxxxxxxxxxxx"
export SENTRY_ORG="your-org"
export SENTRY_PROJECT="your-project"
```

## Installation Requirements

### Zen MCP Server
The zen-server.json configuration assumes zen-mcp-server is installed at:
```
/home/byron/.zen-mcp-server/venv/bin/python
```

If installed elsewhere (e.g., `/home/byron/dev/zen-mcp-server/`), update the path accordingly.

### Docker-based Servers
Some servers like GitHub MCP run via Docker and require Docker to be installed and running.

### Python/Node Servers
Various servers use `uvx`, `npx`, or `uv run` commands and require the respective package managers.

## Troubleshooting

### No MCP Servers Loading
1. Verify `enableAllProjectMcpServers: true` in `settings/base-settings.json`
2. Check that environment variables are set
3. Ensure required executables (python, docker, node, uvx) are available
4. Check Claude Code logs for specific error messages

### Specific Server Not Loading
1. Test the command manually: `${command} ${args[0]} ${args[1]} ...`
2. Verify environment variables for that specific server
3. Check if paths in the configuration file exist

### Common Issues
- **Missing zen-server.json**: This file should exist and be tracked in git
- **Incorrect paths**: Server installation paths may differ from configuration
- **Missing API keys**: External services require valid API credentials
- **Permission issues**: Ensure execute permissions on server binaries

## Validation

Test MCP server loading with:
```bash
claude mcp list
```

Should show all configured and available servers, not just zen.