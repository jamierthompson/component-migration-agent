"""
Component Migration Agent

A multi-agent system for migrating React component libraries
between styling architectures.
"""

from migration_agent.agent import run_migration_agent
from migration_agent.subagents import SUBAGENTS

__all__ = ["run_migration_agent", "SUBAGENTS"]
__version__ = "0.1.0"
