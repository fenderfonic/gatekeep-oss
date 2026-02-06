"""
Gatekeep — AI-powered governance for development teams.

Policy-as-code with specialized AI personas that enforce security,
cost, architecture, and compliance standards.
"""

__version__ = "1.0.0"

from .loader import (
    load_personas,
    load_governance,
    load_standard,
    get_persona_config,
    load_all_for_persona,
)

from .personas import (
    consult_persona,
    consult_sync,
    team_review,
    team_review_sync,
    deployment_gate,
    route_question,
)

__all__ = [
    "load_personas",
    "load_governance",
    "load_standard",
    "get_persona_config",
    "load_all_for_persona",
    "consult_persona",
    "consult_sync",
    "team_review",
    "team_review_sync",
    "deployment_gate",
    "route_question",
]
