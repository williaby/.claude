# MCP Server Loading Issue Analysis

## Problem Summary

The `enableAllProjectMcpServers: true` setting in `/home/byron/.claude/settings/base-settings.json` is not properly loading MCP servers from the global configuration. Only a single zen server loads from project-specific configuration.

## Root Cause Analysis

### 1. Missing Core Configuration File
- **Issue**: No `zen-server.json` tracked in git repository
- **Current State**: File exists locally but is untracked
- **Expected**: Should be part of the base configuration

### 2. Incorrect Zen Server Path Configuration
- **Current Path**: `/home/byron/.zen-mcp-server/venv/bin/python` (in local zen-server.json)
- **Actual Valid Path**: `/home/byron/dev/zen-mcp-server/.zen_venv/bin/python`
- **Problem**: Path points to non-standard installation location

### 3. Configuration Loading Mechanism
- **Expected Behavior**: `enableAllProjectMcpServers: true` should load ALL MCP configurations from `/home/byron/.claude/mcp/*.json`
- **Actual Behavior**: Only zen server loads, others are ignored
- **Missing**: No evidence of a master settings.json that references MCP configurations

### 4. Environment Dependencies
Multiple MCP servers require environment variables that may not be set:
- `GIT_REPO_PATH` (dev-tools-servers.json)
- `GITHUB_PERSONAL_ACCESS_TOKEN` (github-server.json)
- `SERENA_INSTALL_PATH`, `SERENA_PROJECT_PATH` (serena-server.json)
- API keys for external services

## Affected MCP Servers

Based on `/home/byron/.claude/mcp/` directory:
- ✅ **zen**: Loading (but from wrong path)
- ❌ **common-servers**: perplexity, tavily, context7, sentry
- ❌ **dev-tools-servers**: sequential-thinking, git, time
- ❌ **github-server**: github
- ❌ **serena-server**: serena
- ❌ **context7**: http/sse variants
- ❌ **zapier-server**: zapier

## Proposed Solutions

### Immediate Fix
1. Add missing `zen-server.json` to git repository with correct path
2. Ensure all MCP configuration files use standard installation paths
3. Add documentation for required environment variables

### Long-term Fix
1. Investigate why `enableAllProjectMcpServers` mechanism isn't loading all configurations
2. Create environment variable documentation
3. Add validation script to check MCP server availability

## Testing Verification

Before fix:
```bash
claude mcp list
# Shows: zen: /home/byron/dev/zen-mcp-server/.zen_venv/bin/python /home/byron/dev/zen-mcp-server/server.py
```

After fix should show all configured and available MCP servers.

## Files to Modify

1. `/home/byron/.claude/mcp/zen-server.json` - Add to git with correct path
2. Potentially other MCP configurations if paths are incorrect
3. Add documentation for environment variable requirements

## Environment Variables Needed

Document these required variables:
- `GIT_REPO_PATH`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `SERENA_INSTALL_PATH`
- `SERENA_PROJECT_PATH`
- `PERPLEXITY_API_KEY`
- `TAVILY_API_KEY`
- `UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN`
- Additional API keys as needed