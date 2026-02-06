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

# Run setup
./scripts/setup.sh

# Activate environment
source venv/bin/activate

# Make changes and test
./scripts/health-check.sh
```

## Coding Standards

- **Python**: Follow PEP 8
- **Type Hints**: Use type hints where appropriate
- **Documentation**: Update docs for new features
- **Tests**: Add tests for new functionality
- **Commits**: Write clear, descriptive commit messages

## Project Structure

```
gatekeep-intro/
├── core/              # Core governance engine
├── mcp-server/        # MCP integration
├── integrations/      # External integrations (Slack, etc.)
├── governance/        # Policies and standards
├── scripts/           # Setup and utility scripts
└── docs/              # Documentation
```

## Adding New Features

### New Persona

1. Add persona definition to `governance/personas/personas.yaml`
2. Update MCP server to expose new tools
3. Document the persona's role and usage
4. Add tests

### New Standard

1. Create standard directory in `governance/standards/`
2. Add manifest.yaml and control files
3. Update documentation
4. Test with existing personas

### New Integration

1. Create directory in `integrations/`
2. Add README with setup instructions
3. Update main setup script if needed
4. Document integration flow

## Testing

Before submitting a PR:

```bash
# Run health check
./scripts/health-check.sh

# Test MCP integration
# (restart Kiro and test persona consultations)

# Test Slack integration (if applicable)
python integrations/slack/slack_bot.py
```

## Documentation

- Update README.md for user-facing changes
- Update docs/ for detailed documentation
- Add inline code comments for complex logic
- Update CHANGELOG.md

## Questions?

- Open a [Discussion](https://github.com/fenderfonic/gatekeep-oss/discussions)
- Check existing [Issues](https://github.com/fenderfonic/gatekeep-oss/issues)

Thank you for contributing! 🚀
