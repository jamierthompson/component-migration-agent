"""
Component Migration Agent

A multi-agent system for migrating React component libraries
between styling architectures.
"""

from collections.abc import AsyncIterable
from datetime import datetime
from pathlib import Path
from typing import Any

from claude_agent_sdk import query, HookMatcher
from claude_agent_sdk.types import (
    AssistantMessage,
    ClaudeAgentOptions,
    ToolUseBlock,
    UserMessage,
    ResultMessage,
)

from migration_agent.hooks import ToolCallTracker
from migration_agent.subagents import SUBAGENTS

# Ensure output directories exist
FILES_DIR = Path("files")
LOGS_DIR = Path("logs")

ANALYSIS_DIR = FILES_DIR / "analysis"
GENERATED_DIR = FILES_DIR / "generated"
VALIDATION_DIR = FILES_DIR / "validation"

for dir_path in [ANALYSIS_DIR, GENERATED_DIR, VALIDATION_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


LEAD_AGENT_PROMPT = """\
You are the Lead Migration Agent, orchestrating a component library migration.

## Your Role
You coordinate specialized subagents to analyze, transform, and validate
component migrations between styling architectures.

## Available Subagents

1. **style-extractor**: Analyzes source components to extract design tokens
   - Parses inline styles, CSS modules, styled-components, Tailwind classes
   - Maps hardcoded values to semantic token names
   - Outputs: token_map.json, component_inventory.md

2. **pattern-analyzer**: Identifies patterns and variants across components
   - Finds shared styling patterns
   - Documents component variants (size, color, state)
   - Maps props to style variations
   - Outputs: pattern_report.md

3. **code-generator**: Generates migrated component code
   - Creates token definition files (CSS vars, Vanilla Extract, etc.)
   - Transforms components to use new styling approach
   - Preserves existing component API/props
   - Outputs: generated components and token files

4. **diff-validator**: Validates migration completeness and correctness
   - Compares before/after API surfaces
   - Checks for missing styles or tokens
   - Flags breaking changes
   - Outputs: api_diff.md, coverage_report.md, manual_review.md

## Workflow

1. **Discovery**: Use style-extractor to inventory components and extract tokens
2. **Analysis**: Use pattern-analyzer to understand variants and shared patterns
3. **Planning**: Create migration_plan.md with strategy and priorities
4. **Generation**: Use code-generator to produce migrated code
5. **Validation**: Use diff-validator to verify completeness
6. **Report**: Summarize results and flag items needing human review

## Output Locations

- Analysis files: files/analysis/
- Generated code: files/generated/
- Validation reports: files/validation/
- Migration plan: files/migration_plan.md

## Guidelines

- Start by understanding the source architecture before generating anything
- Preserve component APIs—migrations should be non-breaking where possible
- Flag uncertainty rather than guessing (add to manual_review.md)
- Generate incremental output so progress is visible
- Use semantic token names (e.g., `--color-primary` not `--blue-500`)
"""


def create_session_log_dir() -> Path:
    """Create a timestamped session directory for logs."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = LOGS_DIR / f"session_{timestamp}"
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


async def create_prompt_stream(user_prompt: str) -> AsyncIterable[dict[str, Any]]:
    """
    Convert a string prompt to an async iterable for streaming mode.

    Hooks require streaming mode (bidirectional communication) to work.
    The CLI needs to call back to Python for hook execution.
    """
    yield {
        "type": "user",
        "message": {"role": "user", "content": user_prompt},
    }


def format_message(message: AssistantMessage | UserMessage) -> str:
    """Format a message for the transcript."""
    role = "assistant" if isinstance(message, AssistantMessage) else "user"
    content_parts = []

    content = message.content
    if isinstance(content, str):
        content_parts.append(content)
    elif isinstance(content, list):
        for block in content:
            if hasattr(block, "text"):
                content_parts.append(block.text)
            elif hasattr(block, "name"):
                # Tool use block
                content_parts.append(f"[Tool: {block.name}]")

    return f"[{role.upper()}]\n{''.join(content_parts)}\n"


async def run_migration_agent(user_prompt: str) -> None:
    """Run the migration agent with the given prompt."""

    session_dir = create_session_log_dir()
    transcript_path = session_dir / "transcript.txt"

    # Initialize tool call tracker
    tracker = ToolCallTracker(session_dir / "tool_calls.jsonl")

    hooks = {
        "PreToolUse": [HookMatcher(hooks=[tracker.pre_tool_use_hook])],
        "PostToolUse": [HookMatcher(hooks=[tracker.post_tool_use_hook])],
    }

    print(f"\n{'='*60}")
    print("Component Migration Agent")
    print(f"{'='*60}")
    print(f"Session logs: {session_dir}")
    print(f"Output directory: {FILES_DIR}")
    print(f"{'='*60}\n")

    options = ClaudeAgentOptions(
        system_prompt=LEAD_AGENT_PROMPT,
        model="sonnet",
        allowed_tools=[
            "Read",
            "Write",
            "Edit",
            "Glob",
            "Grep",
            "Bash",
            "Task",  # Enables subagents
        ],
        permission_mode="bypassPermissions",
        max_turns=200,
        agents=SUBAGENTS,
        hooks=hooks,
    )

    with open(transcript_path, "w") as transcript:
        transcript.write(f"Session started: {datetime.now().isoformat()}\n")
        transcript.write(f"User prompt: {user_prompt}\n")
        transcript.write("=" * 60 + "\n\n")

        # Use streaming mode (AsyncIterable prompt) to enable hooks
        # Hooks require bidirectional communication between CLI and Python
        async for event in query(
            prompt=create_prompt_stream(user_prompt),
            options=options,
        ):
            if isinstance(event, AssistantMessage):
                # Write to transcript
                formatted = format_message(event)
                transcript.write(formatted)
                transcript.flush()

                # Print text content to console
                if isinstance(event.content, list):
                    for block in event.content:
                        if hasattr(block, "text") and block.text:
                            print(block.text)
                        elif hasattr(block, "name"):
                            tool_block: ToolUseBlock = block
                            if tool_block.name == "Task":
                                subagent = tool_block.input.get("subagent_type", "unknown")
                                print(f"\n🤖 Delegating to: {subagent}")

            elif isinstance(event, UserMessage):
                # Tool results come back as user messages
                formatted = format_message(event)
                transcript.write(formatted)
                transcript.flush()

            elif isinstance(event, ResultMessage):
                if event.is_error:
                    print(f"\nError: {event.result}")

        transcript.write("\n" + "=" * 60 + "\n")
        transcript.write(f"Session ended: {datetime.now().isoformat()}\n")

    print(f"\n{'='*60}")
    print("Migration complete!")
    print(f"{'='*60}")
    print(f"📁 Analysis: {ANALYSIS_DIR}")
    print(f"📁 Generated: {GENERATED_DIR}")
    print(f"📁 Validation: {VALIDATION_DIR}")
    print(f"📁 Logs: {session_dir}")


def main():
    """Interactive entry point."""
    import asyncio

    print("\nComponent Migration Agent")
    print("-" * 40)
    print("Example prompts:")
    print('  "Migrate ./src/components from inline styles to CSS Variables"')
    print('  "Convert the Button component from Tailwind to CSS Modules"')
    print('  "Analyze ./lib and create a token extraction plan"')
    print("-" * 40)

    user_input = input("\nWhat would you like to migrate? \n> ").strip()

    if not user_input:
        print("No input provided. Exiting.")
        return

    asyncio.run(run_migration_agent(user_input))


if __name__ == "__main__":
    main()
