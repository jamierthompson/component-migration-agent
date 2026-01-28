# Component Migration Agent

A multi-agent system that helps migrate React component libraries between styling architectures. Built with the Claude Agent SDK.

## Use Cases

- Inline styles → CSS Variables + CSS Modules
- CSS Modules → Vanilla Extract
- Tailwind → CSS Variables
- styled-components → CSS Modules
- Any combination with custom mappings

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      LEAD AGENT (Orchestrator)                  │
│  Coordinates migration workflow, manages state, generates plan  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│    STYLE      │  │    PATTERN    │  │     CODE      │
│   EXTRACTOR   │  │   ANALYZER    │  │   GENERATOR   │
│               │  │               │  │               │
│ • Parse CSS   │  │ • Find vars   │  │ • Generate    │
│ • Extract     │  │ • Identify    │  │   new styles  │
│   tokens      │  │   variants    │  │ • Transform   │
│ • Map values  │  │ • Group by    │  │   components  │
│   to semantic │  │   component   │  │ • Preserve    │
│   names       │  │ • Document    │  │   API surface │
└───────────────┘  └───────────────┘  └───────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                ┌───────────────────┐
                │   DIFF VALIDATOR  │
                │                   │
                │ • Compare APIs    │
                │ • Check coverage  │
                │ • Flag breaking   │
                │   changes         │
                └───────────────────┘
```

## Quick Start

```bash
# Install dependencies
uv sync

# Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# Run the agent
uv run python migration_agent/agent.py

# Example prompt:
# "Migrate the components in ./src/components from inline styles to CSS Variables"
```

## Output Structure

```
files/
├── analysis/
│   ├── token_map.json          # Extracted design tokens
│   ├── pattern_report.md       # Identified patterns & variants
│   └── component_inventory.md  # List of components to migrate
├── generated/
│   ├── tokens/
│   │   ├── colors.css          # CSS custom properties
│   │   ├── spacing.css
│   │   └── typography.css
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   └── Button.module.css
│   │   └── ...
│   └── index.ts                # Barrel exports
├── validation/
│   ├── api_diff.md             # Breaking changes report
│   ├── coverage_report.md      # What was/wasn't migrated
│   └── manual_review.md        # Items needing human attention
└── migration_plan.md           # Overall migration strategy

logs/
└── session_YYYYMMDD_HHMMSS/
    ├── transcript.txt
    └── tool_calls.jsonl
```

## Configuration

Create a `migration.config.json` in your target project:

```json
{
  "source": {
    "type": "inline-styles",
    "entry": "./src/components"
  },
  "target": {
    "type": "css-variables",
    "tokenOutput": "./src/tokens",
    "componentOutput": "./src/components-v2"
  },
  "options": {
    "preserveInlineForDynamic": true,
    "generateTypeScript": true,
    "cssModules": true
  }
}
```

## Subagent Details

### Style Extractor
Parses existing component files and extracts:
- Hardcoded color values → semantic color tokens
- Spacing values → spacing scale tokens
- Font properties → typography tokens
- Shadow/border values → effect tokens

### Pattern Analyzer
Identifies:
- Component variants (size, color, state)
- Shared patterns across components
- Prop-to-style mappings
- Conditional styling logic

### Code Generator
Produces:
- Token definition files (CSS custom properties, JS objects, or Vanilla Extract)
- Migrated component files with new styling approach
- Updated TypeScript interfaces (preserving existing API)

### Diff Validator
Verifies:
- All original props still work
- No style values were lost
- Breaking changes are documented
- Edge cases are flagged for manual review

## License

MIT
