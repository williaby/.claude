# Global Claude Development Standards

> Universal development standards and practices for Claude Code across all projects.
>
> **Token Optimized**: This streamlined file references detailed specifications in `/standards/` 
> and `/commands/` directories for maximum efficiency while maintaining comprehensive coverage.

## Core Development Standards

> **Detailed Specifications**: See `/standards/python.md`, `/standards/security.md`, `/standards/git-workflow.md`, `/standards/linting.md`

### Essential Requirements
- **Code Quality**: Black formatting (88 chars), Ruff linting, MyPy type checking
- **Security**: GPG/SSH key validation, dependency scanning, encrypted secrets
- **Testing**: Minimum 80% coverage, tiered testing approach
- **Git**: Conventional commits, signed commits, feature branch workflow
- **Response-Aware Development**: Assumption tagging and verification (see `/docs/response-aware-development.md`)

## Response-Aware Development (RAD)

> **Full Documentation**: See `/docs/response-aware-development.md` for complete rationale and evaluation metrics

### Assumption Tagging Standards

When writing code, ALWAYS tag assumptions that could cause production failures:

```javascript
// #CRITICAL: [category]: [assumption that could cause outages/data loss]
// #VERIFY: [defensive code required]
// Example: Payment processing, auth flows, concurrent writes

// #ASSUME: [category]: [assumption that could cause bugs]  
// #VERIFY: [validation needed]
// Example: UI state, form validation, API responses

// #EDGE: [category]: [assumption about uncommon scenarios]
// #VERIFY: [optional improvement]  
// Example: Browser compatibility, slow networks
```

### Critical Assumption Categories (MANDATORY tagging)
- **Timing Dependencies**: State updates, async operations, race conditions
- **External Resources**: API availability, file existence, network connectivity
- **Data Integrity**: Type safety at boundaries, null/undefined handling
- **Concurrency**: Shared state, transaction isolation, deadlock potential
- **Security**: Authentication, authorization, input validation
- **Payment/Financial**: Transaction integrity, retry logic, rollback handling

### Verification Workflow (AUTOMATED with Agent Integration)
1. **During Development**: Claude tags assumptions inline with risk level
2. **On File Save**: Hook triggers assumption-verification-agent scan automatically
3. **Agent Processing**: Agent categorizes, verifies, and suggests defensive fixes
4. **Before Commit**: Agent validates critical assumptions are addressed
5. **Mark Verified**: Agent adds verification timestamps automatically

### File-Type Standards
- **Python**: 88-char line length, comprehensive rule compliance
- **Markdown**: 120-char line length, consistent formatting  
- **YAML**: 2-space indentation, 120-char line length
- **Validation**: Pre-commit hooks enforce all standards

## Essential Commands

> **Complete Command Reference**: See `/commands/quality.md`, `/commands/testing.md`, `/commands/security.md`

### Code Quality & Formatting
```bash
# Format and lint (see /commands/quality.md for full details)
poetry run black .
poetry run ruff check --fix .
poetry run mypy src
markdownlint **/*.md
yamllint **/*.{yml,yaml}
```

### Security Validation
```bash
# Key validation (see /commands/security.md for full details)
gpg --list-secret-keys  # Must show GPG key for .env encryption
ssh-add -l              # Must show SSH key for signed commits
git config --get user.signingkey  # Must be configured for signed commits
poetry run safety check
poetry run bandit -r src
```

### Testing Standards
```bash
# Testing commands (see /commands/testing.md for full details)
poetry run pytest -v --cov=src --cov-report=html --cov-report=term-missing
poetry run pre-commit run --all-files
```

### Assumption Verification (Automated via Agent)
```bash
# Simplified assumption verification commands (replaces complex tooling)
/verify-assumptions              # Agent scans and verifies automatically
/critical-assumptions           # Agent focuses on critical assumptions only  
/apply-assumption-fixes         # Agent applies safe defensive patterns
/assumption-report             # Generate comprehensive assumption analysis report
```

**Agent-Driven Verification Process:**
- **Automatic Detection**: Scans for #CRITICAL, #ASSUME, #EDGE tags in code
- **Risk Categorization**: Routes to appropriate verification strategies
- **Defensive Code Generation**: Creates validation and error handling patterns
- **Hook Integration**: Triggers verification on file save and pre-commit

## OpenSSF Best Practices Compliance

> **Token Optimized**: Existing standards already satisfy most OpenSSF requirements. This section documents compliance mapping and additional requirements.

### Automatic Compliance (Already Configured)
Our existing standards satisfy core OpenSSF requirements:
- ✅ **Testing**: 80% coverage requirement + automated test runs
- ✅ **Static Analysis**: Ruff, MyPy, Bandit already configured
- ✅ **Security Scanning**: Safety check for dependencies
- ✅ **Version Control**: Signed commits, branch protection
- ✅ **Secrets Management**: GPG-encrypted .env files

### Required Project Files (Verify Presence)
```bash
# Check OpenSSF required files exist
ls -1 LICENSE SECURITY.md CONTRIBUTING.md CHANGELOG.md README.md 2>/dev/null | wc -l
# Should output: 5
```

### Release Checklist (Manual Verification)
Before any release:
- [ ] CHANGELOG.md updated with security fixes (if any)
- [ ] No known vulnerabilities >60 days old (`poetry run safety check`)
- [ ] All tests pass with coverage >80%
- [ ] Version tag follows SemVer (vX.Y.Z)
- [ ] Release notes include CVE fixes (if applicable)

### New Feature Requirements
When implementing new functionality:
1. **Add tests first** (TDD when practical)
2. **Document security implications** in docstrings
3. **Update CHANGELOG.md** with user-facing changes
4. **Use established libraries** (don't roll your own crypto)

### Compliance Verification
```bash
# Quick compliance check (available in cookiecutter template)
./scripts/check-openssf.sh

# Weekly automated scorecard (GitHub Actions)
# See .github/workflows/openssf-scorecard.yml in project templates
```

## Project Integration

> **Project Templates**: Use `/templates/python-project.md` or `/templates/general-project.md` for new projects
>
> **Organization Guide**: See `PROJECT-ORGANIZATION-GUIDE.md` for comprehensive guidelines on what should live where in the configuration structure

### Implementation Pattern
Projects create focused `CLAUDE.md` files that **extend** (not duplicate) these global standards:

1. **Reference Pattern**: Use `> Reference: /standards/[domain].md` for detailed requirements
2. **Project Focus**: Include only project-specific configurations and deviations
3. **Inheritance**: All universal standards automatically apply unless overridden

### Example Project Structure
```markdown
# Project Development Guide

> This project extends the global CLAUDE.md standards. Only project-specific 
> configurations and deviations are documented below.

## Project-Specific Standards
> Reference: Global standards apply. Project-specific requirements below.

- **Performance**: API response p95 < 2s
- **Security**: Service account at `.gcp/service-account.json`
- **Architecture**: External Qdrant at 192.168.1.16:6333
```

## Claude Code Supervisor Role (CRITICAL)

**Claude Code acts as the SUPERVISOR for all development tasks and MUST:**

1. **Always Use TodoWrite Tool**: Create and maintain TODO lists for ALL tasks to track progress
2. **Assign Tasks to Agents**: Each TODO item should be assigned to a specialized agent via MCP Server
3. **Review Agent Work**: Validate all agent outputs before proceeding to next steps
4. **Use Temporary Reference Files**: Create `.tmp-` prefixed files in `tmp_cleanup/` folder to store detailed context that might be lost during compaction
5. **Maintain Continuity**: Use reference files to preserve TODO details across conversation compactions

### Agent Assignment Patterns

```bash
# Always assign TODO items to appropriate agents:
- Assumption verification → Assumption Verification Agent (via mcp__zen__assumption-verify)
- Security tasks → Security Agent (via mcp__zen__secaudit)
- Code reviews → Code Review Agent (via mcp__zen__codereview)  
- Testing → Test Engineer Agent (via mcp__zen__testgen)
- Documentation → Documentation Agent (via mcp__zen__docgen)
- Debugging → Debug Agent (via mcp__zen__debug)
- Analysis → Analysis Agent (via mcp__zen__analyze)
- Refactoring → Refactor Agent (via mcp__zen__refactor)
```

### Temporary Reference Files (Anti-Compaction Strategy)

**ALWAYS create temporary reference files when:**
- TODO list contains >5 items
- Complex implementation details need preservation
- Multi-step workflows span multiple conversation turns
- Agent assignments and progress need tracking

**Naming Convention**: `tmp_cleanup/.tmp-{task-type}-{timestamp}.md` (e.g., `tmp_cleanup/.tmp-auth4-implementation-20250125.md`)

### Supervisor Workflow Patterns (MANDATORY)

**Every development task MUST follow this pattern:**

1. **Create TODO List**: Use TodoWrite tool to break down the task into specific, actionable items
2. **Agent Assignment**: Assign each TODO item to the most appropriate specialized agent
3. **Progress Tracking**: Mark items as in_progress when assigned, completed when validated
4. **Reference File Creation**: For complex tasks, create `.tmp-` reference files immediately
5. **Agent Output Validation**: Review all agent work before marking items complete

**For complex tasks requiring multiple agents:**

1. **Sequential Dependencies**: Use TodoWrite to show dependencies between tasks
2. **Parallel Execution**: Assign independent tasks to multiple agents simultaneously
3. **Integration Points**: Create specific TODO items for integrating agent outputs
4. **Quality Gates**: Assign review tasks to appropriate agents after implementation

### PR Preparation Workflow (AUTOMATED)

**ALWAYS use `mcp__zen-core__pr_prepare` tool for PR creation:**

```bash
# Standard PR creation with What the Diff integration
mcp__zen-core__pr_prepare --include_wtd=true --target_branch=main

# Force WTD even for large PRs
mcp__zen-core__pr_prepare --include_wtd=true --force_wtd=true

# Custom parameters
mcp__zen-core__pr_prepare \
  --include_wtd=true \
  --target_branch=main \
  --change_type=feat \
  --title="Add new feature"
```

**Branch Safety and PR Creation MUST follow this pattern:**

1. **Branch Strategy Validation**: Validate current branch strategy and proper targeting
2. **Dependency Validation**: Update poetry.lock and regenerate requirements files automatically
3. **Security Scanning**: Run dependency security checks before PR creation
4. **What the Diff Integration**: Include `<!-- wtd:summary -->` shortcode in PR description
5. **GitHub Integration**: Push branch and create draft PR with comprehensive description
6. **Review Assignment**: Auto-assign reviewers based on CODEOWNERS and change patterns

**Branch Safety Checks:**
- Prevents PRs from main branch (must use feature branches)
- Validates branch naming conventions and targeting strategy
- Provides branch migration assistance for incorrect strategies
- Confirms user intent for main branch targeting

**Automatic PR Generation:**
- Analyzes git commit history and change patterns
- Generates comprehensive PR descriptions with metrics
- **ALWAYS includes What the Diff shortcode** (`<!-- wtd:summary -->`) unless `include_wtd=false`
- Applies appropriate labels based on change types and size
- Integrates with GitHub CLI for seamless workflow

**What the Diff Integration (CRITICAL):**
- **Default behavior**: `include_wtd=true` - WTD shortcode automatically included
- **Shortcode syntax**: `<!-- wtd:summary -->` (HTML comment format)
- **Placement**: Inserted in PR description where AI-generated summary is desired
- **Additional shortcodes**: `<!-- wtd:joke -->`, `<!-- wtd:poem -->` (optional)
- **Large PRs**: Use `--force_wtd=true` to override size-based exclusion
- **Disable WTD**: Set `--include_wtd=false` (rare, only for internal/draft PRs)

## Development Philosophy

**Security First** → **Quality Standards** → **Documentation** → **Testing** → **Collaboration**

### Core Principles
1. **Security First**: Always validate keys, encrypt secrets, scan dependencies
2. **Reuse First**: Check existing repositories for solutions before building new code
3. **Configure, Don't Build**: Prefer configuration and orchestration over custom implementation
4. **Quality Standards**: Maintain consistent code quality across all projects  
5. **Documentation**: Keep documentation current and well-formatted
6. **Testing**: Maintain high test coverage and run tests before commits
7. **Collaboration**: Use consistent Git workflows and clear commit messages

## Pre-Commit Linting Checklist

Before committing ANY changes, ensure:
- [ ] **TODO Management**: Was TodoWrite used for task tracking?
- [ ] **Agent Assignment**: Were tasks assigned to appropriate specialized agents?
- [ ] **Reference Files**: Were temporary reference files created for complex tasks?
- [ ] **Agent Validation**: Was all agent work reviewed and validated?
- [ ] **Assumption Verification**: Agent automatically verified critical assumptions
- [ ] **OpenSSF Compliance**: Required files present (LICENSE, SECURITY.md, CONTRIBUTING.md, CHANGELOG.md)
- [ ] Environment validation passes (GPG and SSH keys present)
- [ ] File-specific linter has been run and passes
- [ ] Pre-commit hooks execute successfully (includes credential leak detection)
- [ ] No linting warnings or errors remain
- [ ] Code formatting is consistent with project standards
- [ ] Commits are signed (Git signing key configured)
- [ ] **Security Scanning**: No known vulnerabilities (`poetry run safety check`)
- [ ] **Branch Safety**: PR preparation validates branch strategy if applicable
- [ ] **Dependency Safety**: Requirements files updated if dependencies changed
- [ ] **PR Creation**: If creating PR, use `mcp__zen-core__pr_prepare` with `--include_wtd=true`

---

*This modular configuration is automatically loaded by Claude Code. For detailed specifications,
see referenced files in `/standards/` and `/commands/` directories.*

*Modularization complete! All detailed specifications are now available in domain-specific files
for maximum token efficiency.*