---
name: workflow-skill-design
description: Designs new Claude Code skills with proper structure, anti-patterns, and reference documentation. Use when creating a new skill or refactoring an existing skill's architecture.
allowed-tools: Read Write Edit Bash Glob Grep
---

# Workflow Skill Design

Designs well-structured Claude Code skills with proper frontmatter, reference architecture, and anti-pattern documentation.

## When to Use

- Creating a new Claude Code skill from scratch
- Redesigning an existing skill's architecture
- Converting an ad-hoc prompt into a reusable skill
- Designing the reference file structure for a complex skill

## Skill Structure Template

```
<skill-name>/
├── skill.md              # Main skill: frontmatter + instructions
└── references/           # Reference files invoked by the skill
    ├── workflow.md       # Step-by-step process (if complex)
    ├── quick-reference.md # Commands and patterns cheat sheet
    └── examples.md       # Concrete examples (good and bad)
```

## Frontmatter Fields

```yaml
---
name: skill-name              # Lowercase, hyphenated. Used for invocation.
description: |                # CRITICAL: Controls when Claude invokes this skill.
  One-line purpose. Use when X. Triggers when seeing Y pattern.
  Include key terms users and code will contain.
allowed-tools: Read Bash Glob Grep Write Edit  # Explicitly list what tools the skill uses
---
```

## Description Field Guidelines

The `description` must answer: "When should Claude use this skill?"

| Pattern | Example |
|---------|---------|
| Use when... | "Use when writing Semgrep rules" |
| Triggers on... | "Triggers when code imports `anthropic`" |
| Activates when... | "Activates when user asks about DWARF" |

Include domain-specific terms that will appear in the user's messages or code.

## Skill Content Structure

```markdown
# Skill Title

One paragraph of purpose and context.

## When to Use
Bullet list of ideal scenarios.

## When NOT to Use
Bullet list of anti-patterns or exclusions.

## Rationalizations to Reject
Common shortcuts users will try to take — with why each is wrong.

## [Core Content]
The actual methodology, workflow, or reference.

## Reference Index
Links to reference files with descriptions.
```

## Rationalizations to Reject Section

This section is **high-value**. Include shortcuts that:
- Save time in the short term but cause bugs later
- Sound reasonable but are actually harmful
- Are things LLMs commonly accept without pushback

Format:
```markdown
## Rationalizations to Reject

- **"[Rationalization]"** → [Why it fails] → [What to do instead]
```

## Reference File Design

Reference files should be:
- **Invoked on-demand**, not loaded upfront (keep skill.md lean)
- **Specific**: Each file covers one topic completely
- **Self-contained**: No circular references between reference files

Reference file types:
- `workflow.md` — Step-by-step processes
- `quick-reference.md` — Commands, syntax, cheat sheets
- `examples.md` — Good and bad patterns with explanations
- `troubleshooting.md` — Common failures and fixes

## Anti-Patterns

**Too much in skill.md**: The skill should be a gateway, not an encyclopedia. Long skills are never fully read.

**No `When NOT to Use` section**: Without explicit exclusions, skills are applied to wrong scenarios.

**Vague descriptions**: "Helps with security" triggers on everything and nothing.

**No rationalizations**: Without explicit shortcuts to reject, LLMs accept them.

**Reference files without links**: If skill.md doesn't link to references, they're never used.
