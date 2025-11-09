# Naming Convention Validation

**Purpose**: Check that code follows Python naming conventions (PEP 8) and project-specific standards.

**Usage**: `/validate-naming [file_path]` or `/validate-naming` (scans src/)

---

## Naming Conventions

### Python Core Conventions (PEP 8)

1. **Modules**: `snake_case.py`
   - Examples: `image_processor.py`, `text_gate.py`
   - Invalid: `ImageProcessor.py`, `textGate.py`

2. **Classes**: `PascalCase`
   - Examples: `DocumentMetadata`, `DetectedIssue`
   - Invalid: `document_metadata`, `detected_Issue`

3. **Functions/Methods**: `snake_case`
   - Examples: `detect_skew()`, `apply_correction()`
   - Invalid: `detectSkew()`, `ApplyCorrection()`

4. **Constants**: `UPPER_SNAKE_CASE`
   - Examples: `DEFAULT_DPI`, `MIN_CONFIDENCE`
   - Invalid: `default_dpi`, `minConfidence`

5. **Private members**: `_leading_underscore`
   - Examples: `_internal_state`, `_validate_input()`
   - Dunder methods: `__init__()`, `__repr__()`

6. **Variables**: `snake_case`
   - Examples: `user_input`, `image_path`
   - Invalid: `userInput`, `ImagePath`

### File and Directory Conventions

1. **Test files**: `test_*.py`
   - Examples: `test_schema.py`, `test_iqa_classical.py`
   - Invalid: `schema_test.py`, `test-schema.py`

2. **Directories**: `snake_case/`
   - Examples: `src/detection/`, `tests/unit/`
   - Invalid: `src/Detection/`, `tests/Unit/`

3. **Git branches**: `kebab-case` with prefixes
   - Examples: `feature/add-layout-detection`, `fix/skew-threshold`
   - Invalid: `feature/add_layout_detection`, `fixSkewThreshold`

---

## Validation Process

### 1. Scan Target Files

```bash
# Single file
find src -name "module.py" -type f

# Entire source tree
find src -type f -name "*.py"
```

### 2. Extract Identifiers

For each Python file, extract:
- Module names (from file path)
- Class definitions: `class (\w+)`
- Function definitions: `def (\w+)`
- Constants: `^([A-Z_]+) =`
- Variables: assignments in module/class scope

### 3. Check Conventions

For each identifier:
- Determine type (module, class, function, constant, variable)
- Apply appropriate naming rule
- Report violations with suggested fixes

---

## Output Format

```
🔤 Naming Convention Validation

📁 src/image_preprocessing_detector/detection/iqa_classical.py

✅ Module name: iqa_classical.py (snake_case)
✅ Class: IQADetector (PascalCase)
✅ Function: detect_skew (snake_case)
✅ Constant: DEFAULT_THRESHOLD (UPPER_SNAKE_CASE)
❌ Variable: ImagePath (line 42)
   Expected: snake_case
   Suggestion: image_path

📁 src/image_preprocessing_detector/schema.py

✅ Class: DocumentMetadata (PascalCase)
❌ Class: detected_issue (line 15)
   Expected: PascalCase
   Suggestion: DetectedIssue

✅ Method: to_json (snake_case)
✅ Method: from_json (snake_case)

---

📊 Summary:
- ✅ 24 correct
- ❌ 2 violations

🎯 Violations to fix:
1. src/.../iqa_classical.py:42 - ImagePath → image_path
2. src/.../schema.py:15 - detected_issue → DetectedIssue
```

---

## Interactive Fix Mode

When violations found, offer to:

1. **Show diff preview**: Display before/after for each violation
2. **Apply fixes**: Use Edit tool to rename identifiers
3. **Update references**: Search for usages and update (with confirmation)
4. **Skip false positives**: Allow exceptions for valid cases (e.g., third-party APIs)

---

## Project-Specific Rules

Check for project-specific CLAUDE.md or CONTRIBUTING.md:

```python
# Load project naming conventions
conventions = read_project_conventions("CLAUDE.md")

# Apply custom rules
if conventions.get("test_prefix") == "test_":
    validate_test_files(pattern="test_*.py")
```

---

## Common Patterns

### Valid Patterns

```python
# Module-level constant
DEFAULT_DPI = 300

# Class with private method
class ImageProcessor:
    def __init__(self):
        self._state = {}

    def process_image(self, image_path: str) -> None:
        self._validate_input(image_path)

    def _validate_input(self, path: str) -> None:
        pass

# Function with local variable
def detect_skew(image: np.ndarray) -> float:
    rotation_angle = 0.0
    return rotation_angle
```

### Invalid Patterns

```python
# ❌ PascalCase for function
def DetectSkew(image: np.ndarray) -> float:
    pass

# ❌ camelCase for variable
def process_image(imagePath: str) -> None:
    pass

# ❌ snake_case for class
class detected_issue:
    pass

# ❌ lowercase for constant
default_dpi = 300
```

---

## Success Criteria

- ✅ All modules use snake_case.py
- ✅ All classes use PascalCase
- ✅ All functions/methods use snake_case
- ✅ All constants use UPPER_SNAKE_CASE
- ✅ Private members use _leading_underscore
- ✅ Test files use test_*.py pattern
- ✅ Git branches use kebab-case with prefixes

**Note**: Suppression comments allowed for third-party API compatibility:
```python
# naming: ignore - matches third-party API
externalAPICall = client.get_data()
```
