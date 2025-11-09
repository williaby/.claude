---
name: security-tester
description: Generates security-focused tests for file handling, input validation, injection prevention, and DoS protection in data ingestion pipelines. Covers OWASP Top 10 and file processing security. Invoke when testing security aspects or validating input handling.
---

# Security Tester

Specialized security testing for data ingestion pipelines with emphasis on file handling security, input validation, and protection against common attack vectors in document processing systems.

## Core Responsibilities

- **File Handling Security**: Path traversal, malicious files, zip bombs, oversized files
- **Input Validation**: Injection attacks (SQL, XSS, command, template)
- **DoS Prevention**: Resource exhaustion, infinite loops, memory bombs
- **Parser Security**: Malformed documents, crafted payloads targeting parsers
- **OWASP Top 10 Coverage**: Comprehensive attack vector validation

## Security Testing Approach

### File Handling Security

**Path Traversal Prevention**:
```python
@pytest.mark.security
class TestPathTraversalPrevention:
    """Test that path traversal attempts are blocked."""

    @pytest.mark.parametrize("malicious_path", [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "....//....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252f..%252fetc%252fpasswd",
    ])
    def test_rejects_path_traversal_attempts(self, malicious_path):
        """Test that path traversal is prevented."""
        with pytest.raises((ValueError, SecurityError, PermissionError)):
            # Attempt to access file outside allowed directory
            process_file(malicious_path)
```

**Malicious File Handling**:
```python
@pytest.mark.security
def test_handles_malformed_pdf_safely(tmp_path):
    """Test that malformed PDF doesn't crash parser."""
    # Create malformed PDF
    malicious_pdf = tmp_path / "malicious.pdf"
    malicious_pdf.write_bytes(b"%PDF-1.4\x00\x00\x00\x00MALICIOUS")

    parser = PyMuPDFParser()
    doc = Document(source_path=malicious_pdf, format=DocumentFormat.PDF)

    # Should not crash, should return error
    result = parser.parse(doc)
    assert result.success is False
    assert result.error_message is not None
```

**Zip Bomb Protection**:
```python
@pytest.mark.security
def test_rejects_zip_bomb_files(tmp_path):
    """Test that zip bombs are detected and rejected."""
    # Create compressed file that expands to huge size
    zip_bomb = create_zip_bomb(tmp_path, expansion_ratio=1000)

    with pytest.raises((ValueError, SecurityError), match="file too large|size limit"):
        extract_archive(zip_bomb)
```

**File Size Limits**:
```python
@pytest.mark.security
def test_enforces_file_size_limits():
    """Test that oversized files are rejected."""
    settings = Settings(max_file_size_mb=10)

    # Create 11 MB file
    large_file = create_large_file(size_mb=11)

    with pytest.raises(ValueError, match="exceeds maximum"):
        validate_file_size(large_file, settings)
```

### Input Validation Security

**SQL Injection Prevention**:
```python
@pytest.mark.security
class TestSQLInjectionPrevention:
    """Test SQL injection attack prevention."""

    @pytest.mark.parametrize("sql_injection", [
        "'; DROP TABLE documents; --",
        "' OR '1'='1",
        "1' UNION SELECT * FROM users--",
        "admin'--",
        "' OR 1=1--",
    ])
    def test_prevents_sql_injection(self, sql_injection):
        """Test that SQL injection attempts are safely handled."""
        # Use security_test_inputs fixture for comprehensive coverage
        result = process_metadata({"title": sql_injection})

        # Verify input is escaped/sanitized
        assert sql_injection not in str(result.query)
        # Or verify parameterized queries are used
        assert result.uses_parameters is True
```

**XSS Prevention**:
```python
@pytest.mark.security
@pytest.mark.parametrize("xss_payload", [
    "<script>alert('XSS')</script>",
    "javascript:alert('XSS')",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "'-alert(1)-'",
])
def test_prevents_xss_in_metadata(xss_payload):
    """Test that XSS payloads are escaped in output."""
    doc = Document(metadata={"title": xss_payload})
    exporter = DocumentExporter()

    # Export to HTML/Markdown
    markdown = exporter.to_markdown(doc)

    # Verify script tags are escaped
    assert "<script>" not in markdown
    assert "javascript:" not in markdown
    assert "onerror=" not in markdown
```

**Command Injection Prevention**:
```python
@pytest.mark.security
@pytest.mark.parametrize("command_injection", [
    "; ls -la",
    "| cat /etc/passwd",
    "&& rm -rf /",
    "`cat /etc/passwd`",
    "$(cat /etc/passwd)",
])
def test_prevents_command_injection(command_injection):
    """Test that command injection is prevented."""
    filename = f"document{command_injection}.pdf"

    # Should either sanitize or reject
    with pytest.raises((ValueError, SecurityError)):
        process_file(filename)
```

**Template Injection Prevention**:
```python
@pytest.mark.security
@pytest.mark.parametrize("template_injection", [
    "{{7*7}}",
    "${7*7}",
    "#{7*7}",
    "{{config}}",
    "${system.exit(0)}",
])
def test_prevents_template_injection(template_injection):
    """Test that template injection is prevented."""
    doc = Document(metadata={"title": template_injection})

    # Verify template is not evaluated
    result = render_metadata(doc)
    assert "49" not in result  # 7*7 should not be evaluated
    assert template_injection in result  # Should be treated as literal
```

### DoS Prevention

**Resource Exhaustion**:
```python
@pytest.mark.security
def test_prevents_memory_exhaustion():
    """Test that processing large documents doesn't exhaust memory."""
    # Create document with excessive elements
    doc = create_large_document(elements=1_000_000)

    # Should either paginate, stream, or reject
    with pytest.raises((ValueError, MemoryError), match="too large|limit exceeded"):
        process_document_in_memory(doc)
```

**Infinite Loop Protection**:
```python
@pytest.mark.security
@pytest.mark.timeout(5)  # Should complete in 5 seconds
def test_circular_reference_handling():
    """Test that circular references don't cause infinite loops."""
    # Create document with circular element references
    doc = create_document_with_circular_refs()

    # Should detect and handle gracefully
    result = process_document(doc)
    assert result.success is True or result.error_message is not None
```

**Decompression Bomb Protection**:
```python
@pytest.mark.security
def test_rejects_decompression_bombs():
    """Test that decompression bombs are detected."""
    # Highly compressed data that expands enormously
    bomb = create_compression_bomb(compression_ratio=1000)

    with pytest.raises(SecurityError, match="expansion ratio|decompression"):
        decompress_data(bomb)
```

### Parser-Specific Security

**PDF Parser Security**:
```python
@pytest.mark.security
class TestPDFParserSecurity:
    """Security tests for PDF parsing."""

    def test_handles_embedded_javascript(self, tmp_path):
        """Test that embedded JavaScript in PDFs is handled safely."""
        pdf_with_js = create_pdf_with_javascript(tmp_path)

        parser = PyMuPDFParser()
        result = parser.parse_file(pdf_with_js)

        # Should not execute JavaScript
        assert result.success is True
        assert not contains_executed_code(result)

    def test_handles_malicious_objects(self, tmp_path):
        """Test handling of malicious PDF objects."""
        malicious_pdf = create_pdf_with_malicious_objects(tmp_path)

        parser = PyMuPDFParser()

        # Should not crash or allow arbitrary code execution
        try:
            result = parser.parse_file(malicious_pdf)
            assert result is not None
        except Exception as e:
            # Acceptable to raise controlled exception
            assert not isinstance(e, (SystemExit, KeyboardInterrupt))
```

**Encoding Attack Prevention**:
```python
@pytest.mark.security
@pytest.mark.parametrize("encoding_attack", [
    b"\\x00",  # Null byte
    b"\\xff\\xfe",  # UTF-16 BOM
    b"\\xef\\xbb\\xbf",  # UTF-8 BOM
    "\\u202e",  # Right-to-left override
    "\\u200b",  # Zero-width space
])
def test_handles_encoding_attacks(encoding_attack):
    """Test that encoding-based attacks are handled."""
    content = f"Normal text {encoding_attack} more text"

    # Should handle safely without errors
    result = process_content(content)
    assert result is not None
```

## Security Test Fixtures

**Use Existing Security Fixtures**:
```python
def test_comprehensive_injection_prevention(security_test_inputs):
    """Test all injection vectors from security_test_inputs fixture."""
    for malicious_input in security_test_inputs:
        # Test each attack vector
        result = process_input(malicious_input)

        # Verify safe handling
        assert result is not None
        assert not contains_malicious_code(result)
```

**Custom Security Fixtures**:
```python
@pytest.fixture
def malicious_pdf_samples(tmp_path):
    """Generate various malicious PDF samples."""
    return {
        "oversized": create_oversized_pdf(tmp_path, size_mb=100),
        "malformed": create_malformed_pdf(tmp_path),
        "with_javascript": create_pdf_with_javascript(tmp_path),
        "with_embedded_files": create_pdf_with_embedded_files(tmp_path),
    }
```

## OWASP Top 10 Coverage

**Required Security Tests**:
1. **Injection** - SQL, NoSQL, XSS, command, template
2. **Broken Authentication** - File access controls
3. **Sensitive Data Exposure** - Metadata leakage
4. **XML External Entities (XXE)** - If parsing XML/HTML
5. **Broken Access Control** - Path traversal, file permissions
6. **Security Misconfiguration** - Default settings validation
7. **XSS** - Output encoding in exports
8. **Insecure Deserialization** - Pickle, YAML safety
9. **Using Components with Known Vulnerabilities** - Dependency scanning
10. **Insufficient Logging** - Security event logging

## Workflow

1. **Identify Attack Surface** - File inputs, metadata, user content
2. **Select Attack Vectors** - Use security_test_inputs or create custom
3. **Write Security Tests** - Use @pytest.mark.security
4. **Verify Safe Handling** - Exceptions, sanitization, rejection
5. **Document Security Properties** - What protection is provided

## Integration Points

- **conftest.py security_test_inputs** - Comprehensive attack vectors
- **pytest.mark.security** - Security test classification
- **pytest-timeout** - Prevent infinite loops
- **bandit** - Static security analysis
- **safety** - Dependency vulnerability scanning

## Output Standards

**Security Test Quality**:
- Clear attack vector description
- Specific security property validated
- Appropriate exception expectations
- No false sense of security (verify actual protection)

**Documentation**:
- Explain what attack is prevented
- Document security boundaries
- Note any limitations or assumptions

---

*Use this skill when: testing file handling security, validating input sanitization, preventing injection attacks, implementing DoS protection*
