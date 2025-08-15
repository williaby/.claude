# Global CLAUDE.md Modularization Plan

## Overview

This document outlines the complete plan to modularize the global CLAUDE.md file for improved token efficiency and maintainability. The current global file consumes ~8,000 tokens in every conversation, which can be reduced to ~1,000 tokens through strategic modularization.

## Current State Analysis

**Token Usage Impact:**
- Global CLAUDE.md: ~8,000 tokens (40-50% of context in typical conversations)
- Project CLAUDE.md (before optimization): ~15,000 tokens 
- Combined impact: ~23,000 tokens (severely limiting working context)

**Content Categories in Current Global CLAUDE.md:**
1. Universal development commands (quality, formatting, security, testing)
2. Universal development standards (code quality, security, Git workflow)
3. File-type specific linting requirements (Python, Markdown, YAML, JSON)
4. Pre-commit linting checklist
5. Development philosophy and practices

## Proposed Modular Structure

```text
.claude/
├── CLAUDE.md (lightweight index - ~1,000 tokens)
├── standards/
│   ├── python.md (Python-specific standards and configurations)
│   ├── security.md (Security requirements, GPG/SSH validation)
│   ├── git-workflow.md (Git standards, branching, commit conventions)
│   └── linting.md (File-type specific linting rules and configurations)
├── commands/
│   ├── quality.md (Code quality and formatting commands)
│   ├── testing.md (Testing commands and strategies)
│   └── security.md (Security scanning and validation commands)
└── templates/
    ├── python-project.md (Python project CLAUDE.md template)
    └── general-project.md (General project CLAUDE.md template)
```

## Implementation Phase Details

### Phase 1: Content Extraction and Modularization

**Step 1: Create Directory Structure**
```bash
mkdir -p ~/.claude/standards
mkdir -p ~/.claude/commands  
mkdir -p ~/.claude/templates
```

**Step 2: Extract Content to Modular Files**

**File: `standards/python.md`**
- Python-specific code quality requirements
- Black formatting configuration (88-character line length)
- Ruff linting rules and configuration
- MyPy type checking requirements
- Test coverage standards (minimum 80%)
- Python version requirements and compatibility

**File: `standards/security.md`**
- GPG key requirements for .env encryption
- SSH key requirements for signed commits
- Key validation procedures and commands
- Dependency security scanning requirements
- Secrets management best practices
- Security scanning tools configuration (Safety, Bandit)

**File: `standards/git-workflow.md`**
- Branch naming conventions
- Conventional Commits format requirements
- PR requirements and linking to issues
- Commit signing requirements
- Code review standards

**File: `standards/linting.md`**
- Markdown linting requirements (.markdownlint.json configuration)
- YAML linting requirements (.yamllint.yml configuration)
- Python linting integration with pyproject.toml
- JSON validation requirements
- Pre-commit hooks configuration

**File: `commands/quality.md`**
- Complete listing of code quality commands
- Format commands (Black, Ruff)
- Linting check commands
- Type checking commands (MyPy)
- Pre-commit hook execution

**File: `commands/testing.md`**
- Test execution commands
- Coverage reporting commands
- Performance testing commands
- Test categorization and markers

**File: `commands/security.md`**
- Key validation commands
- Security scanning commands
- Dependency vulnerability checking
- Environment validation procedures

**Step 3: Create Project Templates**

**File: `templates/python-project.md`**
- Template for Python project CLAUDE.md files
- Standard sections and structure
- Reference patterns to global standards
- Common Python project configurations

**File: `templates/general-project.md`**
- Template for non-Python project CLAUDE.md files
- Universal project structure
- Reference patterns to applicable global standards

### Phase 2: Create Streamlined Global CLAUDE.md

Replace the current comprehensive file with a lightweight index that:

1. **Provides essential context** for immediate use
2. **References detailed specifications** stored in modular files
3. **Maintains backward compatibility** with existing workflows
4. **Uses clear reference patterns** for Claude to understand module relationships

**Key Design Principles:**
- Quick reference information for immediate use
- Clear pointers to detailed specifications
- Consistent reference format: `> Reference: /standards/[domain].md`
- Essential commands with "see [module] for details" patterns
- Development philosophy summary without detailed explanations

### Phase 3: Update Existing Project Files

**For Each Project with CLAUDE.md:**
1. **Review project-specific content** against global standards
2. **Remove redundant sections** that duplicate global standards
3. **Add reference patterns** pointing to global modules
4. **Focus content** on project-unique requirements and configurations
5. **Test functionality** to ensure no loss of development workflow

### Phase 4: Validation and Testing

**Validation Steps:**
1. **Test Claude Code functionality** with modular structure
2. **Verify pre-commit hooks** still function correctly
3. **Validate linting enforcement** across file types
4. **Confirm security requirements** are still enforced
5. **Measure token usage improvement** in typical conversations

## Expected Benefits

### Token Efficiency
- **Global CLAUDE.md reduction**: 8,000 → 1,000 tokens (87.5% reduction)
- **Combined with project optimization**: 23,000 → 2,000 tokens total
- **Context availability**: From 20% to 70%+ available for actual work

### Maintainability Improvements
- **Domain-specific updates**: Update Python standards without affecting security standards
- **Granular version control**: Track changes to specific domains independently
- **Easier auditing**: Review and maintain consistency within focused domains
- **Template-based projects**: Faster setup for new projects with consistent standards

### Development Experience
- **Faster Claude responses**: More context available for actual problem-solving
- **Clearer project setup**: Templates provide consistent starting points
- **Focused documentation**: Find relevant standards quickly in domain-specific files
- **Reduced cognitive load**: Less duplication and redundancy across files

## Migration Strategy

### Low-Risk Rollout
1. **Create modular structure** alongside existing CLAUDE.md
2. **Test with one project** (PromptCraft already optimized)
3. **Validate all functionality** works correctly
4. **Gradual migration** of remaining projects
5. **Full replacement** only after validation

### Rollback Plan
- Keep `CLAUDE.md.backup` for quick restoration
- Modular files can coexist with original structure during testing
- Projects can reference either structure during transition

## Implementation Checklist

### Phase 1: Setup
- [ ] Create directory structure (`standards/`, `commands/`, `templates/`)
- [ ] Extract content from current CLAUDE.md into modular files
- [ ] Create project templates for common project types

### Phase 2: Core Replacement
- [ ] Create streamlined global CLAUDE.md with reference patterns
- [ ] Test functionality with existing projects
- [ ] Validate pre-commit hooks and linting still work

### Phase 3: Project Updates
- [ ] Review and update existing project CLAUDE.md files
- [ ] Remove redundant content and add reference patterns
- [ ] Test each project's development workflow

### Phase 4: Validation
- [ ] Measure token usage improvement in conversations
- [ ] Confirm all development standards are still enforced
- [ ] Document any issues and create solutions

## Success Metrics

**Quantitative:**
- Token usage reduced by 80%+ in typical conversations
- Context availability increased to 70%+ from current 20%
- No loss of functionality in development workflows

**Qualitative:**  
- Easier maintenance of global standards
- Faster project setup using templates
- Clearer separation between universal and project-specific requirements
- Improved Claude Code conversation efficiency

---

**Next Steps:**
1. Create the modular file structure
2. Extract content into domain-specific files
3. Replace global CLAUDE.md with streamlined version
4. Test and validate functionality
5. Optimize remaining project files using the same principles

**Estimated Implementation Time:** 2-3 hours for full migration
**Risk Level:** Low (backups maintained, gradual rollout)
**Impact:** High (significant context efficiency improvement)