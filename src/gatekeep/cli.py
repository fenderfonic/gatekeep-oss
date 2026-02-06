"""Gatekeep CLI — consult personas, run reviews, and manage standards from the terminal."""

import sys
import asyncio

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from .loader import load_personas, load_versions, get_persona_config
from .personas import consult_persona, team_review, deployment_gate, route_question

console = Console()


@click.group()
@click.version_option(package_name="gatekeep")
def cli():
    """Gatekeep — AI governance with specialized personas."""
    pass


@cli.command()
@click.argument("persona")
@click.argument("question", nargs=-1, required=True)
@click.option("--context", "-c", help="Additional context")
def ask(persona: str, question: tuple, context: str):
    """Ask a persona a question.

    Examples:
        gatekeep ask sentinel "Is this IAM policy secure?"
        gatekeep ask auditor "What will this Lambda cost?"
        gatekeep ask architect "Should I use DynamoDB or RDS?"
    """
    question_text = " ".join(question)
    config = get_persona_config(persona.lower())
    if not config:
        console.print(f"[red]Unknown persona: {persona}[/red]")
        console.print("Run [bold]gatekeep personas[/bold] to see available personas.")
        sys.exit(1)

    emoji = config.get("emoji", "👤")
    character = config.get("character", persona)
    console.print(f"\n{emoji} Consulting {character}...\n")

    try:
        response = asyncio.run(consult_persona(persona.lower(), question_text, context))
        console.print(Panel(Markdown(response), title=f"{emoji} {character}"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("content", nargs=-1, required=True)
@click.option("--context", "-c", help="Additional context")
def review(content: tuple, context: str):
    """Run a team review (Auditor + Sentinel + Architect in parallel).

    Example:
        gatekeep review "My deployment plan for the new API"
    """
    content_text = " ".join(content)
    console.print("\n🎯 Running Gatekeep Team Review...\n")

    try:
        results = asyncio.run(team_review(content_text, context))
        for persona_name, response in results.items():
            config = get_persona_config(persona_name)
            emoji = config.get("emoji", "👤") if config else "👤"
            character = config.get("character", persona_name) if config else persona_name
            console.print(Panel(Markdown(response), title=f"{emoji} {character}"))
            console.print()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("plan", nargs=-1, required=True)
@click.option("--env", "-e", required=True, type=click.Choice(["test", "production"]))
@click.option("--context", "-c", help="Additional context")
def deploy(plan: tuple, env: str, context: str):
    """Run a deployment gate check.

    Example:
        gatekeep deploy "New API version 2.0" --env production
    """
    plan_text = " ".join(plan)
    console.print(f"\n🚀 Running Deployment Gate for {env.upper()}...\n")

    try:
        result = asyncio.run(deployment_gate(plan_text, env, context))

        console.print("[bold]Pre-Deployment Checks:[/bold]\n")
        for persona_name, response in result["checks"].items():
            config = get_persona_config(persona_name)
            emoji = config.get("emoji", "👤") if config else "👤"
            character = config.get("character", persona_name) if config else persona_name
            console.print(Panel(Markdown(response), title=f"{emoji} {character}"))

        approver = result["approver"]
        config = get_persona_config(approver)
        emoji = config.get("emoji", "👤") if config else "👤"
        character = config.get("character", approver) if config else approver
        console.print(f"\n[bold]Approval Decision ({env.upper()}):[/bold]\n")
        console.print(Panel(Markdown(result["approval"]), title=f"{emoji} {character}"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("question", nargs=-1, required=True)
def route(question: tuple):
    """Ask Guide to route your question to the right persona.

    Example:
        gatekeep route "I need help with security"
    """
    question_text = " ".join(question)
    console.print("\n🧭 Guide is thinking...\n")

    try:
        persona = asyncio.run(route_question(question_text))
        config = get_persona_config(persona)
        emoji = config.get("emoji", "👤") if config else "👤"
        character = config.get("character", persona) if config else persona
        console.print(f'Guide says: "Talk to {emoji} {character} about that."\n')
        console.print(f'[dim]Run: gatekeep ask {persona} "{question_text}"[/dim]')
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def personas():
    """List available personas."""
    personas_config = load_personas()
    table = Table(title="🎯 Gatekeep Personas")
    table.add_column("", width=3)
    table.add_column("Persona", style="cyan")
    table.add_column("Role")
    table.add_column("Domain")
    table.add_column("Model")

    for name, config in personas_config.get("personas", {}).items():
        model = config.get("model", "unknown")
        if "/" in model:
            model = model.split("/")[-1]
        table.add_row(config.get("emoji", "👤"), name, config.get("role", ""), config.get("domain", ""), model)
    console.print(table)


@cli.group()
def standards():
    """Manage regulatory standards."""
    pass


@standards.command(name="status")
def standards_status():
    """Show status of installed standards."""
    versions = load_versions()
    table = Table(title="📋 Standards Status")
    table.add_column("Standard", style="cyan")
    table.add_column("Installed", style="green")
    table.add_column("Latest", style="yellow")
    table.add_column("Status")

    for sid, info in versions.get("standards", {}).items():
        installed = info.get("installed") or "Not installed"
        latest = info.get("latest", "Unknown")
        status = info.get("status", "unknown")
        style = {
            "current": "[green]✅ Current[/green]",
            "outdated": "[yellow]⚠️ Outdated[/yellow]",
            "not_installed": "[dim]Not installed[/dim]",
        }.get(status, status)
        table.add_row(sid, installed, latest, style)
    console.print(table)


@cli.command()
def init():
    """Initialize Gatekeep in the current project (creates governance/ and gatekeep.yaml)."""
    from pathlib import Path
    import shutil

    pkg_dir = Path(__file__).parent
    cwd = Path.cwd()

    # Copy governance defaults
    for subdir in ["governance", "personas", "standards"]:
        src = pkg_dir / subdir
        dst = cwd / subdir
        if src.exists() and not dst.exists():
            shutil.copytree(src, dst)
            console.print(f"  ✓ Created {subdir}/")
        elif dst.exists():
            console.print(f"  · {subdir}/ already exists, skipping")

    # Create gatekeep.yaml
    yaml_path = cwd / "gatekeep.yaml"
    if not yaml_path.exists():
        yaml_path.write_text(
            'project:\n  name: "my-project"\n  standards:\n    - owasp-top10\n    - cis-aws-2.0\n  governance:\n    budget_limit: 30\n'
        )
        console.print("  ✓ Created gatekeep.yaml")

    # Create .env.example
    env_path = cwd / ".env.example"
    if not env_path.exists():
        env_path.write_text("OPENROUTER_API_KEY=your_openrouter_api_key_here\n")
        console.print("  ✓ Created .env.example")

    console.print("\n🎯 Gatekeep initialized. Set your OPENROUTER_API_KEY and run [bold]gatekeep personas[/bold].")
