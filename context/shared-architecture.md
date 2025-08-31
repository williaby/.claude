# Shared Architecture Patterns

## Core Development Architecture

### Technology Stack

- **Python**: 3.11+ with Poetry dependency management
- **Testing**: pytest with 80%+ coverage requirements
- **Code Quality**: Black (88 chars), Ruff linting, MyPy type checking
- **Security**: GPG/SSH key validation, encrypted secrets, dependency scanning

### Security-First Development

- GPG keys required for .env encryption
- SSH keys required for signed commits
- Git signing key must be configured
- All dependencies scanned with safety/bandit
- No hardcoded secrets or credentials

### File Structure Conventions

- **Python**: snake_case naming for files and functions
- **Markdown**: 120-char line length, consistent formatting
- **YAML**: 2-space indentation, 120-char line length
- **Tests**: Mirror source structure in tests/ directory

### Quality Gates

- All code formatted with Black (88-character line length)
- All code must pass Ruff linting checks
- Type hints required for all functions (MyPy validation)
- Minimum 80% test coverage across all Python modules
- Pre-commit hooks enforce all standards

## PromptCraft-Specific Architecture

### Core Components

- **External Qdrant**: Vector database at 192.168.1.16:6333
- **Zen MCP Server**: Real-time agent orchestration and communication
- **C.R.E.A.T.E. Framework**: Context, Request, Examples, Augmentations, Tone & Format, Evaluation
- **Progressive Journeys**: Four-level user experience (Quick → Templates → IDE → Automation)
- **Knowledge Base**: Structured files in knowledge/ directory with YAML frontmatter

### Integration Points

- **src/core/query_counselor.py**: Query enhancement and routing
- **src/core/hyde_processor.py**: HyDE query transformation
- **src/core/vector_store.py**: External Qdrant integration
- **src/mcp_integration/**: Zen MCP Server communication
- **src/agents/**: Multi-agent system framework
- **knowledge/**: Structured knowledge base with YAML frontmatter

### Performance Requirements

- API response p95 < 2s for all endpoints
- Vector search < 200ms response times
- Agent processing < 5s for complex workflows
- Support 100+ concurrent users
- Memory usage < 2GB per container under load

## Common Design Patterns

### Error Handling

```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise ProcessingError(f"Unable to complete operation: {e}") from e
```

### Async Patterns

```python
async def process_data(data: List[Item]) -> List[Result]:
    async with async_database() as db:
        results = await asyncio.gather(*[
            process_item(item, db) for item in data
        ])
    return results
```

### Configuration Management

- Environment-specific config files
- Encrypted .env files for secrets
- Service account at .gcp/service-account.json
- Feature flags for progressive enhancement
