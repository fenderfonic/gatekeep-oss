"""Persona engine — character-driven LLM specialists that enforce governance and standards."""

import asyncio
import os
from typing import Any, Optional

import aiohttp

from .loader import (
    load_all_for_persona,
    get_persona_config,
    load_personas,
    get_routing_rules,
)


def get_api_key() -> str:
    """Get OpenRouter API key from environment or .env file."""
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key
    # Try local .env
    from pathlib import Path

    for env_path in [Path.cwd() / ".env", Path.home() / ".gatekeep" / ".env"]:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val and val != "your_openrouter_api_key_here":
                        return val
    raise ValueError("OPENROUTER_API_KEY not found. Set it as an environment variable or in a .env file.")


_API_KEY: Optional[str] = None


def build_system_prompt(persona_name: str) -> str:
    """Build the system prompt for a persona, including governance and standards context."""
    data = load_all_for_persona(persona_name)
    if not data:
        raise ValueError(f"Unknown persona: {persona_name}")

    config = data["config"]
    prompt = f"""You are {config["character"]}, providing {config["domain"]} guidance.

CHARACTER TRAITS:
{config["traits"]}

"""
    if data["governance_text"] != "No specific governance rules loaded.":
        mode = config.get("governance_mode", "standard")
        prompt += f"ORGANIZATIONAL GOVERNANCE ({mode.upper()} enforcement):\n{data['governance_text']}\n\n"

    if data["standards_text"] != "No regulatory standards applicable.":
        prompt += f"REGULATORY STANDARDS (MUST ENFORCE):\n{data['standards_text']}\n\n"

    prompt += """RESPONSE STYLE:
- Stay in character with appropriate personality
- Enforce governance and standards strictly
- Provide actionable, domain-specific advice
- Flag violations clearly with control IDs when applicable
- Be helpful but maintain character voice
- Keep responses focused and concise
"""
    return prompt


async def query_llm(model: str, system_prompt: str, user_prompt: str, context: Optional[str] = None) -> str:
    """Query an LLM via OpenRouter."""
    global _API_KEY
    if not _API_KEY:
        _API_KEY = get_api_key()

    message = f"Context: {context}\n\n{user_prompt}" if context else user_prompt

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
            },
            timeout=aiohttp.ClientTimeout(total=60),
        ) as response:
            if response.status != 200:
                text = await response.text()
                raise RuntimeError(f"OpenRouter API error {response.status}: {text}")
            result = await response.json()
            return result["choices"][0]["message"]["content"]


async def consult_persona(persona_name: str, question: str, context: Optional[str] = None) -> str:
    """Consult a persona with a question."""
    config = get_persona_config(persona_name)
    if not config:
        raise ValueError(f"Unknown persona: {persona_name}")

    system_prompt = build_system_prompt(persona_name)
    model = config.get("model", "anthropic/claude-3.5-sonnet")

    if model == "consensus":
        return await _consensus_review(persona_name, question, context)
    return await query_llm(model, system_prompt, question, context)


async def _consensus_review(persona_name: str, question: str, context: Optional[str] = None) -> str:
    """Multi-LLM consensus review (Reviewer's specialty)."""
    config = get_persona_config(persona_name)
    models = config.get("models", ["anthropic/claude-3.5-sonnet", "openai/gpt-4o"])
    system_prompt = build_system_prompt(persona_name)

    tasks = [query_llm(m, system_prompt, question, context) for m in models]
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    emoji = config.get("emoji", "👁️")
    result = f"{emoji} Peer Review (Multi-LLM Consensus)\n\n"
    for model, resp in zip(models, responses):
        name = model.split("/")[-1]
        if isinstance(resp, Exception):
            result += f"**{name}**: Error — {resp}\n\n"
        else:
            result += f"**{name}**:\n{resp}\n\n"
    result += "---\n*Consensus review from multiple perspectives*"
    return result


async def route_question(question: str) -> str:
    """Route a question to the appropriate persona using keyword matching."""
    rules = get_routing_rules()
    keywords = rules.get("keywords", {})
    q = question.lower()

    for keyword, persona in keywords.items():
        if keyword in q:
            if isinstance(persona, list):
                return persona[-1] if ("production" in q or "prod" in q) else persona[0]
            return persona
    return "reviewer"


async def team_review(content: str, context: Optional[str] = None) -> dict[str, str]:
    """Run a parallel team review (Auditor, Sentinel, Architect)."""
    personas_config = load_personas()
    workflow = personas_config.get("workflows", {}).get("team_review", {})

    tasks = {}
    for name, prompt_suffix in workflow.get("personas", {}).items():
        tasks[name] = consult_persona(name, f"{prompt_suffix}: {content}", context)

    results = {}
    responses = await asyncio.gather(*tasks.values(), return_exceptions=True)
    for name, resp in zip(tasks.keys(), responses):
        results[name] = f"Error: {resp}" if isinstance(resp, Exception) else resp
    return results


async def deployment_gate(deployment_plan: str, environment: str, context: Optional[str] = None) -> dict[str, Any]:
    """Run a full deployment gate check with cost, security, and approval stages."""
    check_tasks = {
        "auditor": consult_persona("auditor", f"Cost check for deployment: {deployment_plan}", context),
        "sentinel": consult_persona("sentinel", f"Security check for deployment: {deployment_plan}", context),
    }
    check_responses = await asyncio.gather(*check_tasks.values(), return_exceptions=True)
    checks = dict(zip(check_tasks.keys(), check_responses))

    approver = "guardian" if environment.lower() == "production" else "tester"
    approval_ctx = (
        f"Cost: {checks.get('auditor', 'Error')}\nSecurity: {checks.get('sentinel', 'Error')}\n{context or ''}"
    )
    approval = await consult_persona(
        approver, f"Approve deployment to {environment}?\n\nPlan: {deployment_plan}", approval_ctx
    )

    return {"checks": checks, "approver": approver, "approval": approval, "environment": environment}


# Sync convenience wrappers
def consult_sync(persona_name: str, question: str, context: Optional[str] = None) -> str:
    """Synchronous wrapper for consult_persona."""
    return asyncio.run(consult_persona(persona_name, question, context))


def team_review_sync(content: str, context: Optional[str] = None) -> dict[str, str]:
    """Synchronous wrapper for team_review."""
    return asyncio.run(team_review(content, context))
