# Contributing to Gatekeep

Thank you for your interest in contributing! This document provides guidelines for contributing to Gatekeep.

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to build better governance tools.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/fenderfonic/gatekeep-oss/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

1. Check existing [Issues](https://github.com/fenderfonic/gatekeep-oss/issues) and [Discussions](https://github.com/fenderfonic/gatekeep-oss/discussions)
2. Create a new issue or discussion with:
   - Clear use case
   - Proposed solution
   - Potential impact

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/gatekeep-oss.git
cd gatekeep-oss

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check src/ tests/
ruff format --check src/ tests/
```

## Coding Standards

- **Python**: Follow PEP 8 (enforced by ruff)
- **Type Hints**: Use type hints where appropriate
- **Documentation**: Update docs for new features
- **Tests**: Add tests for new functionality
- **Commits**: Write clear, descriptive commit messages

## Project Structure

```
gatekeep-oss/
├── src/gatekeep/          # Core package
│   ├── __init__.py        # Public API
│   ├── cli.py             # CLI commands
│   ├── loader.py          # YAML config loader
│   ├── personas.py        # Persona engine (LLM integration)
│   ├── governance/        # Bundled governance policies
│   ├── personas/          # Bundled persona definitions
│   └── standards/         # Bundled regulatory standards
├── tests/                 # Test suite
├── governance/            # Example project-level governance
├── personas/              # Example project-level personas
├── standards/             # Example project-level standards
└── pyproject.toml         # Package configuration
```

## Adding New Features

### New Persona

1. Add persona definition to `src/gatekeep/personas/personas.yaml`
2. Include required fields: character, domain, role, model, emoji, traits
3. Assign governance files and standards as needed
4. Add tests
5. Document the persona in README.md

### New Standard

1. Create standard directory in `src/gatekeep/standards/<standard-id>/`
2. Add `manifest.yaml` with standard metadata and file list
3. Add control YAML files referenced in the manifest
4. Update `standards/versions.yaml`
5. Test with `gatekeep standards status`

### New Governance Policy

1. Add YAML file to `src/gatekeep/governance/`
2. Assign to relevant personas in `personas.yaml`
3. Document the policy structure

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_loader.py -v

# Run with coverage
pytest tests/ --cov=gatekeep --cov-report=term-missing
```

## Documentation

- Update README.md for user-facing changes
- Add inline code comments for complex logic
- Update CHANGELOG.md

## Questions?

- Open a [Discussion](https://github.com/fenderfonic/gatekeep-oss/discussions)
- Check existing [Issues](https://github.com/fenderfonic/gatekeep-oss/issues)

Thank you for contributing! 🚀
