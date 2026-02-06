# Security Policy

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Gatekeep, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please email security details to the repository maintainers or use GitHub's private vulnerability reporting feature.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (critical issues prioritized)

## Security Best Practices

When using Gatekeep:

1. **API Keys**: Never commit `.env` files or API keys to version control
2. **Access Control**: Limit who has access to your OpenRouter API keys
3. **Slack Tokens**: Rotate Slack tokens regularly
4. **Updates**: Keep Gatekeep and dependencies up to date
5. **Governance**: Review and customize governance policies for your organization

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Known Security Considerations

- API keys are stored in `.env` files (ensure proper file permissions)
- Slack Socket Mode requires app-level tokens (keep secure)
- OpenRouter API calls contain your code/questions (review OpenRouter's privacy policy)

Thank you for helping keep Gatekeep secure!
