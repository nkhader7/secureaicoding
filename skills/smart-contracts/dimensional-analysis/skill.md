---
name: dimensional-analysis
description: Annotates codebases with unit and dimension analysis to identify arithmetic bugs in DeFi protocols and financial systems with mixed units, precisions, or scaling factors.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Dimensional Analysis

Orchestrates a four-step pipeline to identify dimensional mismatches and arithmetic bugs in code with mixed units, precisions, or scaling factors. Primarily targets DeFi protocols and financial arithmetic systems.

## When to Use

- DeFi protocol security audits
- Financial arithmetic code with mixed units (wei, gwei, tokens, percentages)
- Code with scaling factors, precision conversions, or unit transformations
- When arithmetic bugs are suspected in value calculations

## When NOT to Use

- Non-financial code without unit conversions
- Simple arithmetic without dimensional complexity

## Four-Step Pipeline

### Step 1: Discovery
- Scan the repository to identify arithmetic files
- Build a dimensional vocabulary (units, scaling factors, precision values)
- Persist results to `DIMENSIONAL_SCOPE.json` and `DIMENSIONAL_UNITS.md`

### Step 2: Anchor Annotation
- Add unit comments at key calculation points
- Process through batched annotation agents (parallel for large codebases)
- Output: annotated source with inline unit documentation

### Step 3: Propagation
- Extend annotations through function calls and assignments using dimensional algebra
- Identify potential mismatches where units don't align
- Track scaling operations and precision changes

### Step 4: Validation
- Detect bugs against red-flag patterns and dimensional rules
- Confirm or refute propagated mismatches
- Generate findings report

## Reference Files

- [annotate.md](references/annotate.md) — Annotation syntax and conventions
- [bug-patterns.md](references/bug-patterns.md) — Common dimensional bug patterns
- [common-dimensions.md](references/common-dimensions.md) — Standard unit definitions for DeFi
- [dimension-algebra.md](references/dimension-algebra.md) — Rules for dimensional propagation

## Critical Constraints

- Process ALL in-scope files across ALL priority tiers — no partial analysis
- `DIMENSIONAL_SCOPE.json` is the source of truth for downstream steps
- Vocabulary discovery narrowing never reduces annotation scope
- Terminal `BLOCKED` states must be documented with retry counts
- Analysis concludes only when every in-scope file achieves non-pending status in Steps 2-4

## Common Dimensional Bug Patterns

- **Scale mismatch**: Operating on values in different units without conversion (e.g., wei vs. tokens)
- **Precision loss**: Dividing before multiplying causes truncation errors
- **Missing normalization**: Comparing values with different decimal precisions
- **Overflow**: Intermediate calculations exceed type bounds before scaling down
