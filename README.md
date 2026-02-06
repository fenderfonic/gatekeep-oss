# Gatekeep

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/gatekeep.svg)](https://pypi.org/project/gatekeep/)

**AI-powered governance that explains the "why" behind best practices.**

Gatekeep catches security issues, cost problems, and design anti-patterns before they reach production. Instead of cryptic linter errors, you get conversational explanations from specialized AI personas who help you learn as you build.

```bash
pipx install gatekeep
```

**Alternative installation methods:**
- `pip install gatekeep` (standard Python package)
- Other package managers (Homebrew, Nix, Snap) — [let us know](https://github.com/fenderfonic/gatekeep-oss/issues) if you'd like us to add support!

## Quick Start

```bash
# Install (recommended: use pipx for isolated environment)
pipx install gatekeep

# Set your OpenRouter API key
export OPENROUTER_API_KEY=sk-or-...

# Ask a persona
gatekeep ask sentinel "Is storing passwords in plaintext safe?"
gatekeep ask auditor "What will 3 Lambda functions at 256MB cost monthly?"
gatekeep ask architect "Should I use DynamoDB or RDS for this use case?"

# Run a full team review
gatekeep review "New payment API with Stripe integration"

# Check deployment readiness
gatekeep deploy "API v2.0 release" --env production
```

## The Personas

| Persona | Role | What They Do |
|---------|------|-------------|
| 🧭 **Guide** | Triage | Routes your question to the right specialist |
| 👁️ **Reviewer** | Peer Review | Multi-LLM consensus code review |
| 💰 **Auditor** | Cost Control | Budget enforcement and optimization |
| 🔒 **Sentinel** | Security | Vulnerability detection and hardening |
| 🎨 **Architect** | Design | Architecture patterns and best practices |
| 🧪 **Tester** | Test Gate | Test environment deployment approval |
| 🛡️ **Guardian** | Prod Gate | Production deployment approval |
| 📊 **Observer** | Metrics | Routing, observability, optimization |

Each persona has a distinct personality, enforces specific governance rules, and uses the optimal LLM model for their domain.

## How It Works

Gatekeep uses a two-layer governance model:

```
Your Question
     ↓
┌─────────────────────────────────┐
│  PERSONAS (AI Specialists)      │
│  Sentinel, Auditor, Architect…  │
└─────────────────────────────────┘
     ↓                ↓
┌──────────┐  ┌──────────────────┐
│ Your     │  │ Regulatory       │
│ Policies │  │ Standards        │
│          │  │                  │
│ security │  │ OWASP Top 10    │
│ cost     │  │ CIS AWS 2.0     │
│ arch     │  │ GDPR / SOC 2    │
└──────────┘  └──────────────────┘
```

**Layer 1 — Governance (your rules):** Customizable YAML policies for security, cost control, and architecture that reflect your organization's standards.

**Layer 2 — Standards (external regulations):** Built-in support for OWASP Top 10, CIS AWS 2.0, GDPR, and SOC 2. Personas automatically enforce applicable standards.

## CLI Commands

```bash
gatekeep ask <persona> <question>    # Consult a specific persona
gatekeep review <content>            # Parallel team review (Auditor + Sentinel + Architect)
gatekeep deploy <plan> --env <env>   # Deployment gate check
gatekeep route <question>            # Let Guide pick the right persona
gatekeep personas                    # List all personas
gatekeep standards status            # Show installed standards
gatekeep init                        # Initialize Gatekeep in your project
```

## Project Setup

Initialize Gatekeep in any project to customize governance rules:

```bash
cd my-project
gatekeep init
```

This creates:
- `governance/` — Your security, cost, and architecture policies (editable YAML)
- `personas/` — Persona definitions (add your own or tweak existing ones)
- `standards/` — Regulatory standards (OWASP, CIS, GDPR, SOC 2)
- `gatekeep.yaml` — Project configuration

## Customizing Governance

Edit the YAML files in `governance/` to match your organization:

```yaml
# governance/security.yaml
secrets:
  storage:
    aws:
      primary: "AWS Secrets Manager"
  rotation: "90 days minimum"

encryption:
  in_transit: "TLS 1.2+ required"
  at_rest: "Enable for all storage"
```

```yaml
# governance/cost-control.yaml
budgets:
  global:
    monthly_limit: 100
    currency: "USD"
```

Personas automatically pick up your governance rules and enforce them in their responses.

## Requirements

- Python 3.11+
- [OpenRouter API key](https://openrouter.ai/) (provides access to Claude, GPT-4, and other models)

## Cost Transparency

Gatekeep uses **your** OpenRouter API key — no data leaves your machine, no subscriptions, no vendor lock-in.

**Typical costs:**
- Individual developer: $1-5/month
- Small team (5 people): $10-25/month
- You control the spend (set OpenRouter limits)

**Compare to:**
- GitHub Copilot: $10/user/month ($50/month for 5 people)
- Other AI code review tools: $50-200/month

Gatekeep is cheaper because you only pay for what you use, and we're not trying to extract maximum revenue — we're trying to make governance accessible.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

See [SECURITY.md](SECURITY.md) for reporting vulnerabilities.

## Philosophy

Gatekeep exists because quality code shouldn't be a privilege. Whether you're learning to code, building a side project, or running a startup, you deserve access to the same governance standards that enterprise teams use.

We believe:
- Good practices should be taught, not enforced through fear
- Security and compliance shouldn't require a six-figure budget
- Open source tools should stay open (no bait-and-switch)
- Developers learn best when they understand *why*, not just *what*

## Commercial Use

Gatekeep is MIT licensed — **free for everyone, including commercial use.**

If you're building a business on Gatekeep or using it at work, we'd love to hear from you! Consider:
- ⭐ Starring the repo (helps others discover it)
- 💬 Sharing your story (how Gatekeep helped you)
- 💰 [Sponsoring development](https://github.com/sponsors/fenderfonic) (keeps the project sustainable)
- 🤝 Contributing improvements back (makes it better for everyone)

We're not here to gatekeep governance — we're here to make it accessible.

## Support the Project

Gatekeep is built and maintained by developers who care about making quality code accessible. If it's helped you or your team:

- [GitHub Sponsors](https://github.com/sponsors/fenderfonic)
- [Buy Me a Coffee](https://buymeacoffee.com/fenderfonic)

Every contribution helps us spend more time on Gatekeep and less time on client work.

## License

MIT — see [LICENSE](LICENSE).

---

**Ship safely, not slowly.** 🚀
