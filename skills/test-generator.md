---
name: test-generator
description: DEPRECATED - Migrated to testing skill. Use the testing skill instead, which auto-activates on test-related keywords.
---

# Test Generator (DEPRECATED)

**⚠️ This skill has been deprecated and migrated to the unified testing skill.**

## Migration Notice

This functionality is now available as part of the **testing skill**:

### New Location
`~/.claude/skills/testing/workflows/generate.md`

### How to Use

The testing skill auto-activates when you mention:
- "generate tests"
- "create tests"
- "test coverage"
- "write tests"

Or explicitly invoke: `/testing/generate [module-path]`

### Benefits of New Structure
- **Auto-activation**: No need to remember skill names
- **Integrated workflows**: All testing capabilities in one place
- **Better routing**: Intelligent routing to appropriate workflows
- **Agent integration**: Seamless handoff to test-engineer agent for complex tasks

## Deprecation Timeline

- **Deprecated**: 2025-11-09
- **Removal date**: 2025-12-09 (30 days)
- **Migration path**: Use testing skill

---

*See `~/.claude/skills/testing/SKILL.md` for the new testing skill documentation.*
