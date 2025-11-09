---
category: workflow
complexity: medium
estimated_time: "5-15 minutes"
dependencies: []
version: "1.0"
description: DEPRECATED - Migrated to git skill. Use git skill which auto-activates on git keywords.
---

# Workflow Git Helpers (DEPRECATED)

**⚠️ Deprecated 2025-11-09. Migrated to git skill.**

## New Location
`~/.claude/skills/git/`

## Auto-Activation
The git skill activates on: git, branch, commit, pull request, PR, merge, workflow

## Explicit Usage

- **Branch validation**: `/git/branch validate`
- **Commit validation**: `/git/commit validate`
- **PR readiness**: `/git/pr-check`
- **PR preparation**: `/git/pr-prepare --include_wtd=true`
- **Repository status**: `/git/status`

## Workflows Available

- `skills/git/workflows/branch.md` - Branch management
- `skills/git/workflows/commit.md` - Commit message validation
- `skills/git/workflows/pr-check.md` - PR readiness checks
- `skills/git/workflows/pr-prepare.md` - Automated PR preparation (MCP)
- `skills/git/workflows/status.md` - Repository status

## Removal Date
2025-12-09 (30 days)

---

*See `~/.claude/skills/git/SKILL.md` for new git skill documentation.*
