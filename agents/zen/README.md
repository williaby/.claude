# Zen Agent Implementations - Removed

> **Status**: ⚠️ Files Removed (2025-01-16)
> **Reason**: Project-specific code mixed with global configuration

## What Happened?

The Python files that were previously in this directory (`base_agent.py`, `zen_agent_base.py`, `code_reviewer_agent.py`, etc.) have been removed because they are **project-specific implementations** for the PromptCraft-Hybrid project, not generic global configuration files.

### Files That Were Here

The following 13 Python files were removed:

1. `analysis_agent.py` - (3.4 KB)
2. `base_agent.py` - (17.7 KB) - PromptCraft base agent class
3. `code_reviewer_agent.py` - (14.9 KB)
4. `create_agent.py` - (31.2 KB)
5. `debug_investigator_agent.py` - (18.2 KB)
6. `deep_thinking_agent.py` - (3.6 KB)
7. `documentation_writer_agent.py` - (3.4 KB)
8. `qwen_test_engineer_agent.py` - (2.2 KB)
9. `refactor_specialist_agent.py` - (3.6 KB)
10. `security_auditor_agent.py` - (15.8 KB)
11. `task_integration.py` - (11.7 KB)
12. `test_engineering_agent.py` - (56.3 KB)
13. `zen_agent_base.py` - (13.9 KB)

**Total Size**: ~195 KB of project-specific code

## Why Were They Removed?

These files:

1. **Import from project structure**: Reference `from src.agents.base_agent` which doesn't exist in global config
2. **PromptCraft-specific**: Documented as "for PromptCraft-Hybrid" in docstrings
3. **Will fail outside project**: Cannot run without the PromptCraft project structure
4. **Confuse purpose**: Mix project code with global configuration
5. **Not portable**: Hardcoded to specific project architecture

## Where Should These Files Go?

These implementations belong in the **PromptCraft-Hybrid project repository**, likely at:

```
PromptCraft-Hybrid/
├── src/
│   └── agents/
│       ├── zen/
│       │   ├── __init__.py
│       │   ├── base_agent.py
│       │   ├── zen_agent_base.py
│       │   ├── code_reviewer_agent.py
│       │   ├── debug_investigator_agent.py
│       │   ├── security_auditor_agent.py
│       │   ├── test_engineering_agent.py
│       │   └── ... (other agent implementations)
│       └── ...
└── ...
```

## What Remains in Global Config?

The **agent definition files** (`.md` files) remain in `/home/user/.claude/agents/`:

```
agents/
├── analysis-agent.md
├── assumption-verification-agent.md
├── code-review-agent.md
├── debug-agent.md
├── documentation-agent.md
├── refactor-agent.md
├── security-agent.md
├── test-generator-agent.md
└── ... (other .md definitions)
```

These `.md` files are **generic agent definitions** that:
- Define agent capabilities and interfaces
- Work with any MCP server implementation
- Are portable across projects
- Belong in global configuration

## How to Use Agents Now?

### Via MCP Server (Recommended)

Agent implementations should be accessed through the Zen MCP server:

```bash
# In your PromptCraft project
export ZEN_MCP_SERVER_PATH="$HOME/dev/PromptCraft-Hybrid/zen-mcp-server"
export ZEN_AGENTS_DIR="$HOME/dev/PromptCraft-Hybrid/src/agents/zen"

# Start Claude with MCP
claude
```

### Via Agent Definitions

The `.md` files in `/agents/` define the interface for agents that can be implemented in any project:

```markdown
# agents/code-review-agent.md

Agent definition for code review functionality.
Can be implemented via:
- Zen MCP server
- Direct Python execution
- Claude Code native tools
- External API calls
```

## Recovery (If Needed)

If you need the removed Python files, they are available from:

1. **Git History**: `git log --all --full-history -- agents/zen/*.py`
2. **Previous Commits**: Check commits before 2025-01-16
3. **PromptCraft Project**: Should be the canonical source

To recover a file:

```bash
# Find the commit before removal
git log --all --full-history -- agents/zen/base_agent.py

# Restore from specific commit
git checkout <commit-hash> -- agents/zen/base_agent.py
```

## Lessons Learned

This situation highlights the importance of:

1. **Clear Separation**: Keep global config separate from project code
2. **Documentation**: Mark files as project-specific vs. global
3. **Import Validation**: Check that files can run independently
4. **Regular Audits**: Review configuration for misplaced files

## Related Documentation

- `/docs/agent-integration.md` - How agents integrate with Claude Code
- `/mcp/README.md` - MCP server configuration
- `CLAUDE.md` - Global development standards
- `PROJECT-ORGANIZATION-GUIDE.md` - What belongs where

---

**Last Updated**: 2025-01-16
**Action**: Python implementations removed, .md definitions retained
**Next Steps**: Ensure PromptCraft project has these implementations in proper location
