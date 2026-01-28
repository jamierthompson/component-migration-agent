"""
Hooks for tracking and logging tool calls across agents.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from claude_agent_sdk.types import (
    HookContext,
    PreToolUseHookInput,
    PostToolUseHookInput,
)
from rich.console import Console

console = Console()


class ToolCallTracker:
    """
    Tracks tool calls across the lead agent and all subagents.

    Records:
    - Which agent made the call
    - What tool was used
    - Input parameters
    - Output/result
    - Timing information
    """

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.call_stack: list[str] = []  # Track nested agent calls
        self._spinners: list = []  # Stack of active Status spinners

        # Ensure parent directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize log file
        with open(self.log_path, "w") as f:
            f.write("")  # Create empty file

    def _get_current_agent(self) -> str:
        """Get the name of the currently executing agent."""
        if self.call_stack:
            return self.call_stack[-1]
        return "LEAD"

    def _write_log(self, entry: dict[str, Any]) -> None:
        """Append a log entry to the JSONL file."""
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    async def pre_tool_use_hook(
        self,
        hook_input: PreToolUseHookInput,
        matcher: str | None,
        context: HookContext,
    ) -> dict[str, Any]:
        """
        Called before a tool is executed.

        For Task tools (subagent invocations), we push the subagent
        name onto the call stack.
        """
        tool_name = hook_input["tool_name"]
        tool_input = hook_input["tool_input"]
        agent = self._get_current_agent()

        # Track subagent invocations
        if tool_name == "Task":
            subagent_type = tool_input.get("subagent_type", "unknown")
            self.call_stack.append(subagent_type.upper())

        entry = {
            "type": "pre_tool_use",
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "tool_name": tool_name,
            "tool_input": self._sanitize_input(tool_input),
        }

        self._write_log(entry)

        # Print progress indicator
        if tool_name == "Task":
            subagent = tool_input.get("subagent_type", "subagent")
            console.print(f"  [cyan]↳[/cyan] Starting [bold]{subagent}[/bold]...")
            spinner = console.status(
                f"  [bold cyan]{subagent}[/bold cyan] working...", spinner="dots"
            )
            spinner.start()
            self._spinners.append(spinner)
        elif tool_name in ("Write", "Edit"):
            file_path = tool_input.get("file_path", tool_input.get("path", "unknown"))
            console.print(f"  [dim][{agent}][/dim] [yellow]Writing:[/yellow] {file_path}")
        elif tool_name == "Read":
            file_path = tool_input.get("file_path", tool_input.get("path", "unknown"))
            console.print(f"  [dim][{agent}][/dim] [blue]Reading:[/blue] {file_path}")

        return {}  # Don't modify tool execution

    async def post_tool_use_hook(
        self,
        hook_input: PostToolUseHookInput,
        matcher: str | None,
        context: HookContext,
    ) -> dict[str, Any]:
        """
        Called after a tool completes execution.

        For Task tools, we pop the subagent from the call stack.
        """
        tool_name = hook_input["tool_name"]
        tool_result = hook_input.get("tool_response")
        agent = self._get_current_agent()

        # Pop subagent from stack when Task completes
        if tool_name == "Task" and self.call_stack:
            if self._spinners:
                self._spinners.pop().stop()
            completed_agent = self.call_stack.pop()
            console.print(f"  ✅ Completed [bold]{completed_agent}[/bold]")

        entry = {
            "type": "post_tool_use",
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "tool_name": tool_name,
            "result_summary": self._summarize_result(tool_result),
            "success": not self._is_error_result(tool_result),
        }

        self._write_log(entry)

        return {}  # Don't modify tool result

    def _sanitize_input(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """
        Sanitize tool input for logging.

        Truncates large content to keep logs manageable.
        """
        sanitized = {}

        for key, value in tool_input.items():
            if isinstance(value, str) and len(value) > 500:
                sanitized[key] = value[:500] + f"... [truncated, {len(value)} chars total]"
            else:
                sanitized[key] = value

        return sanitized

    def _summarize_result(self, tool_result: Any) -> str:
        """Create a brief summary of the tool result."""
        if tool_result is None:
            return "None"

        result_str = str(tool_result)

        if len(result_str) > 200:
            return result_str[:200] + f"... [{len(result_str)} chars]"

        return result_str

    def _is_error_result(self, tool_result: Any) -> bool:
        """Check if the tool result indicates an error."""
        if tool_result is None:
            return False

        result_str = str(tool_result).lower()
        error_indicators = ["error", "failed", "exception", "traceback"]

        return any(indicator in result_str for indicator in error_indicators)


class ProgressReporter:
    """
    Optional hook for reporting progress to external systems.

    Could be extended to send webhooks, update a database, etc.
    """

    def __init__(self, callback: Callable | None = None):
        self.callback = callback or self._default_callback
        self.stats = {
            "tools_called": 0,
            "files_written": 0,
            "files_read": 0,
            "subagents_invoked": 0,
        }

    def _default_callback(self, event_type: str, data: dict) -> None:
        """Default callback just prints progress."""
        pass  # Silently track stats

    async def pre_tool_use_hook(
        self,
        hook_input: PreToolUseHookInput,
        matcher: str | None,
        context: HookContext,
    ) -> dict[str, Any]:
        """Track tool usage statistics."""
        tool_name = hook_input["tool_name"]
        self.stats["tools_called"] += 1

        if tool_name == "Task":
            self.stats["subagents_invoked"] += 1
        elif tool_name == "Read":
            self.stats["files_read"] += 1

        self.callback("tool_start", {
            "tool": tool_name,
            "stats": self.stats.copy(),
        })

        return {}

    async def post_tool_use_hook(
        self,
        hook_input: PostToolUseHookInput,
        matcher: str | None,
        context: HookContext,
    ) -> dict[str, Any]:
        """Track completed operations."""
        tool_name = hook_input["tool_name"]
        if tool_name in ("Write", "Edit"):
            self.stats["files_written"] += 1

        self.callback("tool_complete", {
            "tool": tool_name,
            "stats": self.stats.copy(),
        })

        return {}

    def get_summary(self) -> dict[str, int]:
        """Get the current statistics summary."""
        return self.stats.copy()
