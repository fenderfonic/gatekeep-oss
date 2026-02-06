"""Tests for the governance/standards/persona loader."""

import pytest
from pathlib import Path

from gatekeep.loader import (
    load_yaml,
    load_governance,
    load_standard,
    load_personas,
    load_versions,
    get_persona_config,
    get_persona_governance,
    get_persona_standards,
    format_governance_for_prompt,
    format_standards_for_prompt,
    get_routing_rules,
    get_workflows,
    load_all_for_persona,
)


# --- Fixtures ---


@pytest.fixture
def pkg_root():
    """Path to the bundled package config."""
    return Path(__file__).parent.parent / "src" / "gatekeep"


@pytest.fixture
def personas_data():
    return load_personas()


# --- load_yaml ---


def test_load_yaml_missing_file(tmp_path):
    result = load_yaml(tmp_path / "nope.yaml")
    assert result == {}


def test_load_yaml_empty_file(tmp_path):
    f = tmp_path / "empty.yaml"
    f.write_text("")
    assert load_yaml(f) == {}


def test_load_yaml_valid(tmp_path):
    f = tmp_path / "test.yaml"
    f.write_text("key: value\nlist:\n  - a\n  - b\n")
    result = load_yaml(f)
    assert result == {"key": "value", "list": ["a", "b"]}


# --- load_personas ---


def test_load_personas_returns_dict(personas_data):
    assert isinstance(personas_data, dict)
    assert "personas" in personas_data


def test_all_expected_personas_exist(personas_data):
    expected = {"guide", "reviewer", "auditor", "sentinel", "architect", "tester", "guardian", "observer"}
    actual = set(personas_data["personas"].keys())
    assert expected == actual


def test_persona_has_required_fields(personas_data):
    required = {"character", "domain", "role", "model", "emoji", "traits"}
    for name, config in personas_data["personas"].items():
        missing = required - set(config.keys())
        assert not missing, f"Persona '{name}' missing fields: {missing}"


# --- get_persona_config ---


def test_get_persona_config_known():
    config = get_persona_config("sentinel")
    assert config is not None
    assert config["emoji"] == "🔒"
    assert "security" in config["domain"]


def test_get_persona_config_unknown():
    assert get_persona_config("nonexistent") is None


# --- load_governance ---


def test_load_governance_security():
    gov = load_governance(["security.yaml"])
    assert "security.yaml" in gov
    assert "principles" in gov["security.yaml"]


def test_load_governance_all_files():
    gov = load_governance(["security.yaml", "cost-control.yaml", "architecture.yaml"])
    assert len(gov) == 3


def test_load_governance_missing_file():
    gov = load_governance(["does-not-exist.yaml"])
    assert gov == {}


# --- load_standard ---


def test_load_standard_owasp():
    std = load_standard("owasp-top10")
    assert "manifest" in std
    assert "domains" in std
    assert std["manifest"]["standard"]["id"] == "owasp-top10"


def test_load_standard_cis():
    std = load_standard("cis-aws-2.0")
    assert "manifest" in std
    assert "iam" in std["domains"]


def test_load_standard_gdpr():
    std = load_standard("gdpr")
    assert "manifest" in std
    assert "data-protection" in std["domains"]


def test_load_standard_unknown():
    assert load_standard("fake-standard") == {}


# --- get_persona_governance / standards ---


def test_sentinel_has_security_governance():
    gov = get_persona_governance("sentinel")
    assert "security.yaml" in gov


def test_auditor_has_cost_governance():
    gov = get_persona_governance("auditor")
    assert "cost-control.yaml" in gov


def test_sentinel_has_standards():
    std = get_persona_standards("sentinel")
    assert "cis-aws-2.0" in std
    assert "owasp-top10" in std


def test_unknown_persona_governance():
    assert get_persona_governance("nobody") == {}


def test_unknown_persona_standards():
    assert get_persona_standards("nobody") == {}


# --- format_governance_for_prompt ---


def test_format_governance_empty():
    assert format_governance_for_prompt({}) == "No specific governance rules loaded."


def test_format_governance_includes_content():
    gov = load_governance(["security.yaml"])
    text = format_governance_for_prompt(gov)
    assert "security.yaml" in text
    assert len(text) > 100


# --- format_standards_for_prompt ---


def test_format_standards_empty():
    assert format_standards_for_prompt({}) == "No regulatory standards applicable."


def test_format_standards_includes_controls():
    std = get_persona_standards("sentinel")
    text = format_standards_for_prompt(std)
    assert "OWASP" in text or "CIS" in text


# --- routing ---


def test_routing_rules_exist():
    rules = get_routing_rules()
    assert "keywords" in rules
    assert "security" in rules["keywords"]


def test_routing_security_goes_to_sentinel():
    rules = get_routing_rules()
    assert rules["keywords"]["security"] == "sentinel"


def test_routing_cost_goes_to_auditor():
    rules = get_routing_rules()
    assert rules["keywords"]["cost"] == "auditor"


# --- workflows ---


def test_workflows_exist():
    wf = get_workflows()
    assert "team_review" in wf
    assert "deployment_gate" in wf


# --- load_all_for_persona ---


def test_load_all_sentinel():
    data = load_all_for_persona("sentinel")
    assert "config" in data
    assert "governance" in data
    assert "standards" in data
    assert "governance_text" in data
    assert "standards_text" in data
    assert data["config"]["emoji"] == "🔒"


def test_load_all_unknown():
    assert load_all_for_persona("nobody") == {}


# --- load_versions ---


def test_load_versions():
    versions = load_versions()
    assert "standards" in versions
    assert "owasp-top10" in versions["standards"]
