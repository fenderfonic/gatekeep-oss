"""Tests for the persona engine — prompt building, routing, and workflow logic."""

import pytest
from unittest.mock import AsyncMock, patch

from gatekeep.personas import (
    build_system_prompt,
    route_question,
    consult_persona,
    team_review,
    deployment_gate,
    consult_sync,
    team_review_sync,
)


# --- build_system_prompt ---


def test_build_prompt_sentinel():
    prompt = build_system_prompt("sentinel")
    assert "Sentinel" in prompt
    assert "security" in prompt.lower()
    assert "GOVERNANCE" in prompt or "governance" in prompt.lower()
    assert "STANDARDS" in prompt or "standards" in prompt.lower()


def test_build_prompt_auditor():
    prompt = build_system_prompt("auditor")
    assert "Auditor" in prompt
    assert "cost" in prompt.lower()


def test_build_prompt_guide_no_governance():
    prompt = build_system_prompt("guide")
    assert "Guide" in prompt
    # Guide has no governance files, so no governance section
    assert "No specific governance rules loaded" not in prompt or "GOVERNANCE" not in prompt


def test_build_prompt_unknown_raises():
    with pytest.raises(ValueError, match="Unknown persona"):
        build_system_prompt("nonexistent")


def test_build_prompt_includes_traits():
    prompt = build_system_prompt("architect")
    assert "Architect" in prompt
    assert "TRAITS" in prompt or "traits" in prompt.lower()


def test_build_prompt_reviewer_no_governance():
    """Reviewer has no governance files but does have standards."""
    prompt = build_system_prompt("reviewer")
    assert "Reviewer" in prompt


# --- route_question ---


@pytest.mark.asyncio
async def test_route_security_to_sentinel():
    result = await route_question("Is this security configuration safe?")
    assert result == "sentinel"


@pytest.mark.asyncio
async def test_route_cost_to_auditor():
    result = await route_question("What will this cost?")
    assert result == "auditor"


@pytest.mark.asyncio
async def test_route_design_to_architect():
    result = await route_question("How should I design this API?")
    assert result == "architect"


@pytest.mark.asyncio
async def test_route_code_to_reviewer():
    result = await route_question("Can you review this code?")
    assert result == "reviewer"


@pytest.mark.asyncio
async def test_route_deploy_test():
    result = await route_question("Can I deploy to staging?")
    assert result == "tester"


@pytest.mark.asyncio
async def test_route_deploy_production():
    result = await route_question("Deploy to production please")
    assert result == "guardian"


@pytest.mark.asyncio
async def test_route_unknown_defaults_to_reviewer():
    result = await route_question("Something completely unrelated to any keyword")
    assert result == "reviewer"


# --- consult_persona (mocked LLM) ---


@pytest.mark.asyncio
async def test_consult_persona_calls_llm():
    with patch("gatekeep.personas.query_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Mocked response from Sentinel"
        result = await consult_persona("sentinel", "Is this safe?")
        assert result == "Mocked response from Sentinel"
        mock_llm.assert_called_once()
        # Verify system prompt was built for sentinel
        call_args = mock_llm.call_args
        assert "sentinel" in call_args[0][1].lower() or "Sentinel" in call_args[0][1]


@pytest.mark.asyncio
async def test_consult_persona_with_context():
    with patch("gatekeep.personas.query_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Response with context"
        result = await consult_persona("auditor", "Cost?", context="Lambda 256MB")
        assert result == "Response with context"
        mock_llm.assert_called_once()


@pytest.mark.asyncio
async def test_consult_unknown_persona_raises():
    with pytest.raises(ValueError, match="Unknown persona"):
        await consult_persona("nobody", "Hello?")


@pytest.mark.asyncio
async def test_consult_reviewer_uses_consensus():
    """Reviewer model is 'consensus' — should call _consensus_review."""
    with patch("gatekeep.personas._consensus_review", new_callable=AsyncMock) as mock_consensus:
        mock_consensus.return_value = "Consensus result"
        result = await consult_persona("reviewer", "Review this code")
        assert result == "Consensus result"
        mock_consensus.assert_called_once()


# --- team_review (mocked) ---


@pytest.mark.asyncio
async def test_team_review_returns_all_personas():
    with patch("gatekeep.personas.consult_persona", new_callable=AsyncMock) as mock_consult:
        mock_consult.return_value = "Looks good"
        results = await team_review("New payment API")
        # Should have auditor, sentinel, architect
        assert "auditor" in results
        assert "sentinel" in results
        assert "architect" in results


@pytest.mark.asyncio
async def test_team_review_handles_errors():
    async def side_effect(name, question, context=None):
        if name == "sentinel":
            raise RuntimeError("API error")
        return "OK"

    with patch("gatekeep.personas.consult_persona", side_effect=side_effect):
        results = await team_review("Test content")
        assert "Error" in results["sentinel"]
        assert results["auditor"] == "OK"


# --- deployment_gate (mocked) ---


@pytest.mark.asyncio
async def test_deployment_gate_production():
    with patch("gatekeep.personas.consult_persona", new_callable=AsyncMock) as mock_consult:
        mock_consult.return_value = "Approved"
        result = await deployment_gate("API v2", "production")
        assert result["environment"] == "production"
        assert result["approver"] == "guardian"
        assert "checks" in result
        assert "approval" in result


@pytest.mark.asyncio
async def test_deployment_gate_test():
    with patch("gatekeep.personas.consult_persona", new_callable=AsyncMock) as mock_consult:
        mock_consult.return_value = "Ship it"
        result = await deployment_gate("API v2", "test")
        assert result["approver"] == "tester"


# --- sync wrappers ---


def test_consult_sync():
    with patch("gatekeep.personas.query_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Sync response"
        result = consult_sync("sentinel", "Is this safe?")
        assert result == "Sync response"


def test_team_review_sync():
    with patch("gatekeep.personas.consult_persona", new_callable=AsyncMock) as mock_consult:
        mock_consult.return_value = "OK"
        results = team_review_sync("Content")
        assert isinstance(results, dict)
