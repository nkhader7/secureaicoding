---
name: variant-analysis
description: Finds similar vulnerabilities across codebases after identifying an initial pattern. Use when you have a known bug and want to find related instances throughout a codebase.
allowed-tools: Bash Read Glob Grep WebFetch
---

# Variant Analysis

Systematically find similar vulnerabilities across a codebase after identifying an initial bug pattern.

## When to Use

- You have a confirmed vulnerability and want to find similar instances
- Performing a security audit where one bug suggests others
- Verifying a fix was applied consistently across a codebase
- Building detection rules from a real vulnerability

## When NOT to Use

- General security scanning without a seed vulnerability
- Finding unrelated classes of bugs
- Code quality reviews

## Core Methodology

See [methodology.md](references/methodology.md) for the complete philosophy and workflow.

**Five-Step Process:**

1. **Understand the original issue**: Identify root cause, required conditions, exploitability
2. **Create exact matches**: Use ripgrep to verify you've found only the known instance
3. **Identify abstraction points**: Which code elements stay specific vs. get generalized?
4. **Iteratively generalize**: Change ONE element at a time, validate results
5. **Analyze results**: Document location, confidence level, and exploitability for each match

## Root Cause Statement

Before searching, formulate a clear statement:

> "This vulnerability exists because [UNTRUSTED DATA] reaches [DANGEROUS OPERATION] without [REQUIRED PROTECTION]."

This statement IS your search pattern.

## Tool Selection

| Scenario | Tool |
|----------|------|
| Quick recon / exact string search | `ripgrep` |
| Simple syntactic patterns | `Semgrep` |
| Complex data flow analysis | `CodeQL` |

## Abstraction Ladder

Start at Level 0 and climb one step at a time:

| Level | Description | FP Rate |
|-------|-------------|---------|
| 0 | Exact match (literal code) | ~0% |
| 1 | Variable abstraction (different var names) | Low |
| 2 | Structural abstraction (same pattern) | Medium |
| 3 | Semantic abstraction (taint tracking) | High |

**Rule**: Never jump more than one level at a time. Measure false positives at each step.

## Common Mistakes

- **Narrow search scope**: Only searching the module with the original bug misses variants elsewhere
- **Overly specific patterns**: Using exact function names misses semantically related constructs
- **Single vulnerability class**: One manifestation overlooks other ways the same logic error appears
- **Missing edge cases**: Testing only "normal" scenarios bypasses boundary condition bugs

## Expanding Vulnerability Classes

For each root cause, check:

1. What other attributes/functions have similar semantics?
2. What other boolean logic errors could occur? (inverted conditions, wrong defaults)
3. What edge cases exist? (null, empty, zero, boundary values)
4. What documentation mismatches could exist? (function does opposite of docstring)
