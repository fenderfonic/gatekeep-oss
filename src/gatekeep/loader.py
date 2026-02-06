"""Configuration loader for governance policies, standards, and persona definitions."""

import yaml
from pathlib import Path
from typing import Any, Optional


def _find_config_root() -> Path:
    """Find the configuration root directory.

    Searches for governance files in this order:
    1. ./governance/ (project-local)
    2. Package-bundled defaults
    """
    cwd = Path.cwd()
    if (cwd / "governance").is_dir():
        return cwd
    # Fall back to package-bundled config
    return Path(__file__).parent


def _get_paths() -> tuple[Path, Path, Path, Path]:
    """Return (base, governance, standards, personas) paths."""
    base = _find_config_root()
    return base, base / "governance", base / "standards", base / "personas"


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file, returning empty dict if missing."""
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_governance(files: list[str]) -> dict[str, Any]:
    """Load governance policies from specified filenames."""
    _, governance_dir, _, _ = _get_paths()
    governance = {}
    for filename in files:
        path = governance_dir / filename
        if path.exists():
            governance[filename] = load_yaml(path)
    return governance


def load_standard(standard_id: str) -> dict[str, Any]:
    """Load a complete regulatory standard by ID."""
    _, _, standards_dir, _ = _get_paths()
    standard_dir = standards_dir / standard_id
    if not standard_dir.exists():
        return {}

    manifest = load_yaml(standard_dir / "manifest.yaml")
    if not manifest:
        return {}

    standard: dict[str, Any] = {"manifest": manifest, "domains": {}}
    for filename in manifest.get("standard", {}).get("files", []):
        domain_path = standard_dir / filename
        if domain_path.exists():
            domain_name = filename.replace(".yaml", "")
            standard["domains"][domain_name] = load_yaml(domain_path)
    return standard


def load_personas() -> dict[str, Any]:
    """Load persona definitions."""
    _, _, _, personas_dir = _get_paths()
    return load_yaml(personas_dir / "personas.yaml")


def load_versions() -> dict[str, Any]:
    """Load standards version tracking."""
    _, _, standards_dir, _ = _get_paths()
    return load_yaml(standards_dir / "versions.yaml")


def get_persona_config(persona_name: str) -> Optional[dict[str, Any]]:
    """Get configuration for a specific persona."""
    personas = load_personas()
    return personas.get("personas", {}).get(persona_name)


def get_persona_governance(persona_name: str) -> dict[str, Any]:
    """Load governance files assigned to a persona."""
    config = get_persona_config(persona_name)
    if not config:
        return {}
    return load_governance(config.get("governance", []))


def get_persona_standards(persona_name: str) -> dict[str, Any]:
    """Load standards assigned to a persona."""
    config = get_persona_config(persona_name)
    if not config:
        return {}
    standards = {}
    for standard_id in config.get("standards", []):
        standard = load_standard(standard_id)
        if standard:
            standards[standard_id] = standard
    return standards


def format_governance_for_prompt(governance: dict[str, Any]) -> str:
    """Format governance rules for inclusion in an LLM prompt."""
    if not governance:
        return "No specific governance rules loaded."
    sections = []
    for filename, content in governance.items():
        sections.append(f"# {filename}")
        sections.append(yaml.dump(content, default_flow_style=False))
    return "\n\n".join(sections)


def format_standards_for_prompt(standards: dict[str, Any]) -> str:
    """Format regulatory standards for inclusion in an LLM prompt."""
    if not standards:
        return "No regulatory standards applicable."
    sections = []
    for standard_id, content in standards.items():
        manifest = content.get("manifest", {}).get("standard", {})
        sections.append(f"# {manifest.get('name', standard_id)} (v{manifest.get('version', 'unknown')})")
        for domain_name, domain_content in content.get("domains", {}).items():
            sections.append(f"\n## {domain_name}")
            for control in domain_content.get("controls", [])[:10]:
                ctrl_id = control.get("id", "")
                requirement = control.get("requirement", "")
                severity = control.get("severity", "")
                sections.append(f"- [{ctrl_id}] ({severity}) {requirement}")
    return "\n".join(sections)


def get_routing_rules() -> dict[str, Any]:
    """Get keyword routing rules for the Guide persona."""
    personas = load_personas()
    return personas.get("routing", {})


def get_workflows() -> dict[str, Any]:
    """Get composite workflow definitions."""
    personas = load_personas()
    return personas.get("workflows", {})


def load_all_for_persona(persona_name: str) -> dict[str, Any]:
    """Load everything needed for a persona: config, governance, standards, and formatted prompts."""
    config = get_persona_config(persona_name)
    if not config:
        return {}
    gov = get_persona_governance(persona_name)
    std = get_persona_standards(persona_name)
    return {
        "config": config,
        "governance": gov,
        "standards": std,
        "governance_text": format_governance_for_prompt(gov),
        "standards_text": format_standards_for_prompt(std),
    }
