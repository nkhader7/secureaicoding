---
name: mutation-testing
description: Mutation testing campaign configuration using mewt/muton. Use when the user mentions "mewt", "muton", or needs to configure or optimize a mutation testing campaign.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Mutation Testing

Campaign configuration for mutation testing using mewt (general-purpose languages) and muton (TON smart contracts).

> **Note**: `mewt` and `muton` share identical interfaces. `mewt` targets Rust, Solidity, Go, TypeScript, JavaScript. `muton` targets TON smart contracts (Tact, Tolk, FunC). All examples use `mewt` commands but work identically with `muton`.

## When to Use

- User mentions "mewt", "muton", or "mutation testing"
- Configuring or optimizing a mutation testing campaign
- User wants to run `mewt run` and needs setup help

## When NOT to Use

- Analyzing or reporting on COMPLETED campaign results
- Questions about tests or coverage without mentioning mutation testing

## Quick Start

Load [workflows/configuration.md](references/optimization-strategies.md) — a 5-phase guide from `mewt init` to a validated, ready-to-run campaign.

For unfamiliar commands, run `mewt --help` or `mewt <subcommand> --help`.

## Essential Commands

```bash
# Initialize and mutate
mewt init                    # Create mewt.toml and mewt.sqlite
mewt mutate [paths]          # Generate mutants without running tests
mewt run [paths]             # Run the full campaign

# Inspect configuration and scope
mewt print config            # View effective configuration
mewt print targets           # Table of all targeted files
mewt print mutations --language [lang]  # Available mutation types
mewt status                  # Mutant count and per-file breakdown

# Investigate specific mutants
mewt print mutants --target [path]   # All mutants for a file
mewt print mutants --severity high   # Filter by severity
mewt print mutant --id [id]          # View mutated code diff
mewt test --ids [ids]                # Re-test specific mutants
```

## Understanding Results

| Status | Meaning |
|--------|---------|
| **Caught/TestFail** | Tests detected the mutation (good) |
| **Uncaught** | Mutation survived — indicates untested logic |
| **Timeout** | Tests took too long, inconclusive |
| **Skipped** | A more severe mutant already failed on the same line |

## Optimization Reference

See [optimization-strategies.md](references/optimization-strategies.md) for:
- Per-file targeting to reduce campaign scope
- Two-phase campaigns for integration-heavy test suites
- Mutation type filtering by severity level

## Basic Configuration (`mewt.toml`)

```toml
[targets]
include = ["src/**/*.rs"]
ignore = ["test", "mock", "generated"]

[test]
cmd = "cargo test"
timeout = 60

[run]
# Optional: Restrict to high/medium severity mutations
# mutations = ["ER", "CR", "IF", "IT"]
```
