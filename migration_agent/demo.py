"""
Demo mode for recording videos.

This script simulates the migration agent's terminal output
without actually running the agent. Perfect for creating
demo videos where timing and output can be controlled.
"""

import asyncio

from rich.console import Console, RenderableType
from rich.padding import Padding
from rich.table import Table
from rich.tree import Tree
from rich import box

from migration_agent.banner import print_banner, print_phase, PAD, LEFT_PAD

console = Console()


def pprint(content: RenderableType, **kwargs):
    """Print any content with left padding."""
    console.print(Padding(content, LEFT_PAD), **kwargs)


# Simulated file operations for the demo
DEMO_SCENARIO = {
    "source_files": [
        "src/components/Button.tsx",
        "src/components/Card.tsx",
        "src/components/Input.tsx",
        "src/components/Modal.tsx",
        "src/components/Badge.tsx",
        "src/components/Avatar.tsx",
    ],
    "tokens_extracted": [
        ("--color-primary", "#3B82F6"),
        ("--color-primary-hover", "#2563EB"),
        ("--color-secondary", "#6B7280"),
        ("--color-success", "#10B981"),
        ("--color-error", "#EF4444"),
        ("--spacing-sm", "8px"),
        ("--spacing-md", "16px"),
        ("--spacing-lg", "24px"),
        ("--radius-sm", "4px"),
        ("--radius-md", "8px"),
        ("--font-size-sm", "14px"),
        ("--font-size-md", "16px"),
    ],
    "patterns_found": [
        "Button variants: primary, secondary, danger, ghost",
        "Size variants: sm, md, lg (padding + font-size)",
        "Hover states: color shift + shadow elevation",
        "Focus rings: consistent 2px offset outline",
        "Disabled state: 50% opacity + cursor not-allowed",
    ],
    "generated_files": [
        "files/generated/tokens/colors.css",
        "files/generated/tokens/spacing.css",
        "files/generated/tokens/typography.css",
        "files/generated/components/Button.tsx",
        "files/generated/components/Button.module.css",
        "files/generated/components/Card.tsx",
        "files/generated/components/Card.module.css",
        "files/generated/components/Input.tsx",
        "files/generated/components/Input.module.css",
    ],
    "validation_results": {
        "api_parity": "100% - All props preserved",
        "token_coverage": "12/12 tokens mapped",
        "breaking_changes": "0 breaking changes detected",
        "manual_review": "2 items flagged for review",
    },
}


async def type_text(text: str, delay: float = 0.03, style: str | None = None) -> None:
    """Simulate typing text character by character."""
    console.print(PAD, end="")
    for char in text:
        console.print(char, end="", style=style, highlight=False)
        await asyncio.sleep(delay)
    console.print()


async def run_demo(speed: float = 1.0) -> None:
    """
    Run the demo simulation.

    Args:
        speed: Multiplier for animation speed (0.5 = faster, 2.0 = slower)
    """

    def delay(base: float) -> float:
        return base * speed

    # Clear screen and scrollback buffer, then show banner
    print("\033[2J\033[3J\033[H", end="", flush=True)
    print_banner()
    await asyncio.sleep(delay(2.0))

    # Show session info
    pprint("[dim]Session:[/dim] logs/session_demo")
    pprint("[dim]Output:[/dim]  files/\n")
    await asyncio.sleep(delay(0.5))

    # Simulated user input
    pprint("[bold]Migration Request:[/bold]")
    await type_text(
        '"Migrate ./src/components from inline styles to CSS Variables + Modules"',
        delay=delay(0.02),
        style="dim italic"
    )
    console.print()
    await asyncio.sleep(delay(0.8))

    # Lead agent thinking
    pprint("Analyzing migration request and planning workflow...\n")
    await asyncio.sleep(delay(1.0))

    # PHASE 1: Style Extraction
    print_phase("extract")
    await asyncio.sleep(delay(1.0))

    with console.status("[bold cyan]style-extractor[/bold cyan] working...", spinner="dots"):
        for file in DEMO_SCENARIO["source_files"]:
            pprint(f"[dim][STYLE-EXTRACTOR][/dim] [blue]Reading:[/blue] {file}")
            await asyncio.sleep(delay(0.3))

        await asyncio.sleep(delay(0.5))
        pprint("\nExtracting design tokens...\n")
        await asyncio.sleep(delay(0.5))

        pprint(f"[dim][STYLE-EXTRACTOR][/dim] [yellow]Writing:[/yellow] files/analysis/token_map.json")
        await asyncio.sleep(delay(0.4))
        pprint(f"[dim][STYLE-EXTRACTOR][/dim] [yellow]Writing:[/yellow] files/analysis/component_inventory.md")
        await asyncio.sleep(delay(0.4))

    pprint("✅ Completed [bold cyan]STYLE-EXTRACTOR[/bold cyan]")

    # Show extracted tokens
    pprint("\n[bold]Tokens Extracted:[/bold]")
    token_table = Table(box=box.ROUNDED, border_style="dim")
    token_table.add_column("Token", style="cyan")
    token_table.add_column("Value", style="yellow")
    for token, value in DEMO_SCENARIO["tokens_extracted"][:6]:
        token_table.add_row(token, value)
    token_table.add_row("...", f"+{len(DEMO_SCENARIO['tokens_extracted']) - 6} more")
    pprint(token_table)
    await asyncio.sleep(delay(1.0))

    # PHASE 2: Pattern Analysis
    print_phase("analyze")
    await asyncio.sleep(delay(1.0))

    with console.status("[bold yellow]pattern-analyzer[/bold yellow] working...", spinner="dots"):
        pprint(f"[dim][PATTERN-ANALYZER][/dim] [blue]Reading:[/blue] files/analysis/token_map.json")
        await asyncio.sleep(delay(0.5))

        for file in DEMO_SCENARIO["source_files"][:3]:
            pprint(f"[dim][PATTERN-ANALYZER][/dim] [blue]Reading:[/blue] {file}")
            await asyncio.sleep(delay(0.25))

        await asyncio.sleep(delay(0.8))
        pprint(f"[dim][PATTERN-ANALYZER][/dim] [yellow]Writing:[/yellow] files/analysis/pattern_report.md")
        await asyncio.sleep(delay(0.3))

    pprint("✅ Completed [bold yellow]PATTERN-ANALYZER[/bold yellow]")

    # Show patterns
    pprint("\n[bold]Patterns Identified:[/bold]")
    for pattern in DEMO_SCENARIO["patterns_found"]:
        pprint(f"• {pattern}", style="dim")
        await asyncio.sleep(delay(0.2))
    await asyncio.sleep(delay(0.8))

    # PHASE 3: Code Generation
    print_phase("generate")
    await asyncio.sleep(delay(1.0))

    with console.status("[bold green]code-generator[/bold green] working...", spinner="dots"):
        pprint(f"[dim][CODE-GENERATOR][/dim] [blue]Reading:[/blue] files/analysis/token_map.json")
        await asyncio.sleep(delay(0.3))
        pprint(f"[dim][CODE-GENERATOR][/dim] [blue]Reading:[/blue] files/analysis/pattern_report.md")
        await asyncio.sleep(delay(0.3))

        pprint("\nGenerating migrated components...\n")
        await asyncio.sleep(delay(0.5))

        for file in DEMO_SCENARIO["generated_files"]:
            pprint(f"[dim][CODE-GENERATOR][/dim] [yellow]Writing:[/yellow] {file}")
            await asyncio.sleep(delay(0.25))

        await asyncio.sleep(delay(0.3))

    pprint("✅ Completed [bold green]CODE-GENERATOR[/bold green]")
    await asyncio.sleep(delay(0.8))

    # PHASE 4: Validation
    print_phase("validate")
    await asyncio.sleep(delay(1.0))

    with console.status("[bold magenta]diff-validator[/bold magenta] working...", spinner="dots"):
        for file in ["Button.tsx", "Card.tsx", "Input.tsx"]:
            pprint(f"[dim][DIFF-VALIDATOR][/dim] [blue]Reading:[/blue] src/components/{file}")
            await asyncio.sleep(delay(0.2))
            pprint(f"[dim][DIFF-VALIDATOR][/dim] [blue]Reading:[/blue] files/generated/components/{file}")
            await asyncio.sleep(delay(0.2))

        await asyncio.sleep(delay(0.5))

        pprint(f"[dim][DIFF-VALIDATOR][/dim] [yellow]Writing:[/yellow] files/validation/api_diff.md")
        await asyncio.sleep(delay(0.3))
        pprint(f"[dim][DIFF-VALIDATOR][/dim] [yellow]Writing:[/yellow] files/validation/coverage_report.md")
        await asyncio.sleep(delay(0.3))
        pprint(f"[dim][DIFF-VALIDATOR][/dim] [yellow]Writing:[/yellow] files/validation/manual_review.md")
        await asyncio.sleep(delay(0.3))

    pprint("✅ Completed [bold magenta]DIFF-VALIDATOR[/bold magenta]")
    await asyncio.sleep(delay(0.5))

    # Show validation results
    pprint("\n[bold]Validation Results:[/bold]")
    for key, value in DEMO_SCENARIO["validation_results"].items():
        icon = "✅" if "100%" in value or "0 breaking" in value else "⚠️"
        pprint(f"{icon} {key}: [bold]{value}[/bold]")
        await asyncio.sleep(delay(0.3))

    # COMPLETION
    await asyncio.sleep(delay(0.8))
    console.print()
    print_phase("complete")

    # Show output tree
    tree = Tree("[bold]📁 Output[/bold]")
    analysis = tree.add("📂 files/analysis/")
    analysis.add("[cyan]token_map.json[/cyan]")
    analysis.add("[cyan]component_inventory.md[/cyan]")
    analysis.add("[cyan]pattern_report.md[/cyan]")

    generated = tree.add("📂 files/generated/")
    tokens = generated.add("📂 tokens/")
    tokens.add("[yellow]colors.css[/yellow]")
    tokens.add("[yellow]spacing.css[/yellow]")
    tokens.add("[yellow]typography.css[/yellow]")
    components = generated.add("📂 components/")
    components.add("[green]Button.tsx + Button.module.css[/green]")
    components.add("[green]Card.tsx + Card.module.css[/green]")
    components.add("[green]Input.tsx + Input.module.css[/green]")

    validation = tree.add("📂 files/validation/")
    validation.add("[magenta]api_diff.md[/magenta]")
    validation.add("[magenta]coverage_report.md[/magenta]")
    validation.add("[magenta]manual_review.md[/magenta]")

    pprint(tree)
    console.print()

    # Final stats
    pprint("[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
    pprint("[bold]Migration Summary[/bold]")
    pprint(f"• Components migrated: [bold cyan]6[/bold cyan]")
    pprint(f"• Design tokens extracted: [bold cyan]12[/bold cyan]")
    pprint(f"• Files generated: [bold cyan]9[/bold cyan]")
    pprint(f"• API compatibility: [bold green]100%[/bold green]")
    pprint("[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")


def main():
    """Entry point for the demo."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run a simulated demo of the Component Migration Agent"
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Speed multiplier (0.5 = faster, 2.0 = slower). Default: 1.0"
    )

    args = parser.parse_args()
    asyncio.run(run_demo(speed=args.speed))


if __name__ == "__main__":
    main()
