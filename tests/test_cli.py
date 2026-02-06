"""Tests for the CLI interface."""

import pytest
from unittest.mock import patch, AsyncMock
from click.testing import CliRunner

from gatekeep.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


# --- personas command ---


def test_personas_list(runner):
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0
    assert "Gatekeep Personas" in result.output
    assert "sentinel" in result.output.lower() or "Sentinel" in result.output


# --- standards status ---


def test_standards_status(runner):
    result = runner.invoke(cli, ["standards", "status"])
    assert result.exit_code == 0
    assert "Standards Status" in result.output


# --- init command ---


def test_init_creates_files(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert "initialized" in result.output.lower() or "Created" in result.output


def test_init_idempotent(runner, tmp_path):
    """Running init twice shouldn't fail."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        runner.invoke(cli, ["init"])
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert "already exists" in result.output or "skipping" in result.output.lower()


# --- ask command ---


def test_ask_unknown_persona(runner):
    result = runner.invoke(cli, ["ask", "nobody", "hello"])
    assert result.exit_code != 0
    assert "Unknown persona" in result.output


def test_ask_calls_persona(runner):
    with patch("gatekeep.cli.consult_persona", new_callable=AsyncMock) as mock:
        mock.return_value = "Test response from Sentinel"
        result = runner.invoke(cli, ["ask", "sentinel", "Is this safe?"])
        assert result.exit_code == 0
        assert "Sentinel" in result.output


# --- review command ---


def test_review_calls_team(runner):
    with patch("gatekeep.cli.team_review", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "auditor": "Cost looks fine",
            "sentinel": "Security OK",
            "architect": "Design approved",
        }
        result = runner.invoke(cli, ["review", "New API"])
        assert result.exit_code == 0
        assert "Team Review" in result.output


# --- deploy command ---


def test_deploy_requires_env(runner):
    result = runner.invoke(cli, ["deploy", "API v2"])
    assert result.exit_code != 0


def test_deploy_calls_gate(runner):
    with patch("gatekeep.cli.deployment_gate", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "checks": {"auditor": "OK", "sentinel": "OK"},
            "approver": "guardian",
            "approval": "Approved",
            "environment": "production",
        }
        result = runner.invoke(cli, ["deploy", "API v2", "--env", "production"])
        assert result.exit_code == 0
        assert "Deployment Gate" in result.output


# --- route command ---


def test_route_calls_router(runner):
    with patch("gatekeep.cli.route_question", new_callable=AsyncMock) as mock:
        mock.return_value = "sentinel"
        result = runner.invoke(cli, ["route", "security question"])
        assert result.exit_code == 0
        assert "Sentinel" in result.output


# --- version ---


def test_version(runner):
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output
