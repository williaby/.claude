# Pre-Commit Validation with Interactive Fixes

**Purpose**: Run all pre-commit checks locally with Claude's help to fix issues before committing.

**Usage**: `/validate-precommit` or `/validate-precommit --fix`

---

## Validation Checklist

Execute the following checks in order, stopping at the first failure:

### 1. Code Formatting (Black)

```bash
poetry run black --check src tests
```

**If fails**: Run `poetry run black src tests` and show diff summary

### 2. Linting (Ruff)

```bash
poetry run ruff check src tests
```

**If fails**: Run `poetry run ruff check --fix src tests` and report remaining issues

### 3. Type Checking (MyPy)

```bash
poetry run mypy src
```

**If fails**:
- Show type errors with file paths and line numbers
- Suggest fixes for common patterns:
  - Missing type hints → Add annotations
  - Optional handling → Add None checks
  - Import errors → Verify module structure

### 4. Security Scanning (Bandit)

```bash
poetry run bandit -r src
```

**If fails**:
- Show security issues with CWE classifications
- Suggest secure alternatives
- Determine if `# nosec` is appropriate with justification

### 5. Dependency Security (Safety)

```bash
poetry run safety check
```

**If fails**:
- Show vulnerable packages with CVE details
- Suggest version updates: `poetry add package@^X.Y.Z`
- Check if vulnerabilities affect production code

### 6. Test Suite

```bash
poetry run pytest -v --cov=src --cov-report=term-missing --cov-fail-under=80
```

**If fails**:
- Show failing tests with full tracebacks
- Identify coverage gaps
- Suggest test additions for uncovered code

### 7. Pre-commit Hooks

```bash
poetry run pre-commit run --all-files
```

**If fails**: Show hook-specific errors and re-run after fixes

---

## Interactive Fix Mode

When `--fix` flag is provided or user confirms:

1. **Auto-fix formatters**: Black, Ruff auto-fix
2. **Suggest type hints**: For MyPy errors
3. **Propose security fixes**: For Bandit issues
4. **Update dependencies**: For Safety vulnerabilities
5. **Generate missing tests**: For coverage gaps

---

## Output Format

```
🔍 Pre-Commit Validation Report

✅ Code Formatting (Black)
✅ Linting (Ruff) - 3 issues auto-fixed
❌ Type Checking (MyPy) - 2 errors found

📍 src/module.py:42
   error: Argument 1 has incompatible type "str | None"; expected "str"

   💡 Suggested Fix:
   if value is not None:
       process(value)

✅ Security Scanning (Bandit)
⚠️  Dependency Security (Safety) - 1 vulnerability

   📦 requests 2.28.0 → 2.31.0 (CVE-2023-32681)

   💡 Fix: poetry add requests@^2.31.0

⏭️  Skipped: Tests (due to MyPy failure)
⏭️  Skipped: Pre-commit hooks (due to MyPy failure)

---

🎯 Next Steps:
1. Fix MyPy type errors in src/module.py:42
2. Update requests dependency
3. Re-run validation
```

---

## Success Criteria

All checks pass:
- ✅ Black formatting compliant
- ✅ Ruff linting passes
- ✅ MyPy type checking passes
- ✅ No Bandit security issues
- ✅ No Safety vulnerabilities
- ✅ Tests pass with ≥80% coverage
- ✅ Pre-commit hooks pass

**Ready to commit**: Git signing verification message displayed

---

## Configuration Detection

Auto-detect project configuration:
- Check for `pyproject.toml` (Poetry project)
- Check for `.pre-commit-config.yaml`
- Check for `pytest.ini` or `pyproject.toml [tool.pytest]`
- Verify `poetry.lock` exists

If not Poetry project, adapt commands for pip/venv.
