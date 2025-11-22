#!/bin/bash
# Claude Code startup script with git-trackable configuration
# Usage: ./start-claude.sh [args...]

export CLAUDE_CONFIG_DIR="$HOME/.claude"
exec claude "$@"