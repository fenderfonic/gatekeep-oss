# Gatekeep

Archived February 2026 experiment exploring accessible governance configuration and LLM-assisted development guidance. This repository is unmaintained and preserved as a historical engineering experiment. It is not recommended as a production security or compliance control.

## What the implementation does

- Loads local YAML governance policies, standards references and persona definitions, using project-local configuration when a `governance/` directory exists, otherwise bundled defaults.
- Lists configuration and routes questions using local keyword matching. Local policy/configuration loading does not require an API key or external inference.
- Optionally consults AI personas, runs team reviews and generates advisory responses about deployment plans through OpenRouter.

AI-backed commands (`ask`, `review` and `deploy`) send the applicable system prompt, formatted governance/standards configuration, user input and supplied context to OpenRouter for the configured model. Team and multi-model reviews can make multiple requests. The deployment-plan review also passes earlier model responses into a subsequent request. These operations are not local-only.

## Limits

The implementation provides advisory guidance, not deterministic compliance enforcement. Language such as “enforce”, “gate” or “approval” in historical prompts and configuration describes requested model behaviour; it does not establish an enforceable control. The `deploy` command prints model responses and does not deploy software or reliably block a deployment.

The bundled standards YAML is experimental reference material, not a complete or maintained implementation of OWASP, CIS, GDPR or SOC 2 requirements. Model responses may be incomplete or incorrect. There is no certification, security guarantee or supported production integration. Using this library from another workflow does not make that workflow a compliance gate.

## Repository reference

- [Configuration loader](src/gatekeep/loader.py)
- [OpenRouter requests and persona workflows](src/gatekeep/personas.py)
- [CLI](src/gatekeep/cli.py)
- [Security and data handling](SECURITY.md)
- [Contribution status](CONTRIBUTING.md)

Historical model identifiers and dependencies are preserved; their current availability is not guaranteed. No ongoing maintenance or support is offered. Licensed under [MIT](LICENSE).
