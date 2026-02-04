"""
ASCII art banner for the Component Migration Agent.
"""

from rich.console import Console
from rich.padding import Padding

# Left padding for terminal output
PAD = "  "
LEFT_PAD = (0, 0, 0, len(PAD))

# ASCII art banner - shows transformation/migration concept
BANNER = r"""
   _____ ___  __  __ ____   ___  _   _ _____ _   _ _____
  / ____/ _ \|  \/  |  _ \ / _ \| \ | | ____| \ | |_   _|
 | |   | | | | |\/| | |_) | | | |  \| |  _| |  \| | | |
 | |___| |_| | |  | |  __/| |_| | |\  | |___| |\  | | |
  \____|\___/|_|  |_|_|    \___/|_| \_|_____|_| \_| |_|

  __  __ ___ ____ ____      _  _____ ___ ___  _   _
 |  \/  |_ _/ ___|  _ \    / \|_   _|_ _/ _ \| \ | |
 | |\/| || | |  _| |_) |  / _ \ | |  | | | | |  \| |
 | |  | || | |_| |  _ <  / ___ \| |  | | |_| | |\  |
 |_|  |_|___\____|_| \_\/_/   \_\_| |___\___/|_| \_|

     _    ____ _____ _   _ _____
    / \  / ___| ____| \ | |_   _|
   / _ \| |  _|  _| |  \| | | |
  / ___ \ |_| | |___| |\  | | |
 /_/   \_\____|_____|_| \_| |_|

"""

# Phase headers for demo
PHASE_EXTRACT = r"""
 ____  _         _        _____      _                  _   _
/ ___|| |_ _   _| | ___  | ____|_  _| |_ _ __ __ _  ___| |_(_) ___  _ __
\___ \| __| | | | |/ _ \ |  _| \ \/ / __| '__/ _` |/ __| __| |/ _ \| '_ \
 ___) | |_| |_| | |  __/ | |___ >  <| |_| | | (_| | (__| |_| | (_) | | | |
|____/ \__|\__, |_|\___| |_____/_/\_\\__|_|  \__,_|\___|\__|_|\___/|_| |_|
           |___/
"""

PHASE_ANALYZE = r"""
 ____       _   _                        _                _           _
|  _ \ __ _| |_| |_ ___ _ __ _ __       / \   _ __   __ _| |_   _ ___(_)___
| |_) / _` | __| __/ _ \ '__| '_ \     / _ \ | '_ \ / _` | | | | / __| / __|
|  __/ (_| | |_| ||  __/ |  | | | |   / ___ \| | | | (_| | | |_| \__ \ \__ \
|_|   \__,_|\__|\__\___|_|  |_| |_|  /_/   \_\_| |_|\__,_|_|\__, |___/_|___/
                                                            |___/
"""

PHASE_GENERATE = r"""
  ____          _         ____                           _   _
 / ___|___   __| | ___   / ___| ___ _ __   ___ _ __ __ _| |_(_) ___  _ __
| |   / _ \ / _` |/ _ \ | |  _ / _ \ '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \
| |__| (_) | (_| |  __/ | |_| |  __/ | | |  __/ | | (_| | |_| | (_) | | | |
 \____\___/ \__,_|\___|  \____|\___|_| |_|\___|_|  \__,_|\__|_|\___/|_| |_|

"""

PHASE_VALIDATE = r"""
__     __    _ _     _       _   _
\ \   / /_ _| (_) __| | __ _| |_(_) ___  _ __
 \ \ / / _` | | |/ _` |/ _` | __| |/ _ \| '_ \
  \ V / (_| | | | (_| | (_| | |_| | (_) | | | |
   \_/ \__,_|_|_|\__,_|\__,_|\__|_|\___/|_| |_|

"""

PHASE_COMPLETE = r"""
 __  __ _                 _   _               ____                      _      _       _
|  \/  (_) __ _ _ __ __ _| |_(_) ___  _ __   / ___|___  _ __ ___  _ __ | | ___| |_ ___| |
| |\/| | |/ _` | '__/ _` | __| |/ _ \| '_ \ | |   / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \ |
| |  | | | (_| | | | (_| | |_| | (_) | | | || |__| (_) | | | | | | |_) | |  __/ ||  __/_|
|_|  |_|_|\__, |_|  \__,_|\__|_|\___/|_| |_| \____\___/|_| |_| |_| .__/|_|\___|\__\___(_)
          |___/                                                  |_|
"""

PHASES = {
    "extract": PHASE_EXTRACT,
    "analyze": PHASE_ANALYZE,
    "generate": PHASE_GENERATE,
    "validate": PHASE_VALIDATE,
    "complete": PHASE_COMPLETE,
}


def print_banner() -> None:
    """Print the ASCII art banner to the console."""
    console = Console()

    lines = BANNER.split("\n")

    # Color gradient from cyan to blue
    colors = ["bright_cyan", "cyan", "blue", "bright_blue", "blue", "cyan", "bright_cyan"]

    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        console.print(Padding(line, LEFT_PAD), style=color, highlight=False)

    console.print()


def print_phase(phase: str) -> None:
    """
    Print a phase header to the console.

    Args:
        phase: One of "extract", "analyze", "generate", "validate", or "complete"
    """
    console = Console()
    phase_text = PHASES.get(phase, "")

    if not phase_text:
        return

    lines = phase_text.split("\n")

    # Phase-specific colors
    phase_colors = {
        "extract": "cyan",
        "analyze": "yellow",
        "generate": "green",
        "validate": "magenta",
        "complete": "bright_green",
    }
    color = phase_colors.get(phase, "white")

    for line in lines:
        console.print(Padding(line, LEFT_PAD), style=color, highlight=False)

    console.print()
