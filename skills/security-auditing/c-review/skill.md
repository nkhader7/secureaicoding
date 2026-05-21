---
name: c-review
description: Orchestrates a multi-phase security code review for C/C++ codebases using parallel specialized agents. Use when performing a security audit of C or C++ code.
allowed-tools: Bash Read Write Glob Grep
---

# C/C++ Security Review

Orchestrates a native C/C++ security auditing workflow through Claude agents, performing deterministic parallel vulnerability analysis across memory safety, integer overflow, race conditions, and platform-specific attack surfaces.

## When to Use

- Security audit of C or C++ codebases
- Pre-release security review of native code
- Finding memory safety bugs, integer overflows, race conditions
- Platform-specific security review (POSIX, Windows)

## When NOT to Use

- Kernel drivers/modules (specialized analysis required)
- Managed-language applications (Java, Python, Go, Rust, C#)
- Bare-metal embedded code without libc

## Architecture

A multi-stage pipeline:
1. **Coordinator** spawns M specialized worker agents in parallel
2. Workers analyze file clusters independently
3. **Judge agent** deduplicates findings across workers
4. **FP judge** filters false positives and assigns severity ratings
5. **SARIF generator** produces machine-readable output

All bookkeeping uses a task ledger; workers are stateless and communicate through markdown files in a shared output directory.

## Nine-Phase Orchestration

| Phase | Action |
|-------|--------|
| 0 | Collect threat model, worker model selection, severity filtering |
| 1 | Probe for C++ source, POSIX headers, Windows APIs |
| 2 | Create output directory structure |
| 3 | Read repository metadata, write context documentation |
| 4 | Delegate cluster selection to `build_run_plan.py` → `plan.json` |
| 5 | Create bookkeeping task per worker |
| 6 | Spawn all M workers in one parallel batch |
| 7 | Classify worker outcomes, construct findings-index |
| 8 | Dedup-judge merges duplicates, fp-judge assesses false positives |
| 9 | Validate success criteria, return final report |

## Key Design Principles

- Workers spawn **foreground** (not background) — parallelism achieved by multiple `Agent` calls in a single message
- Never re-derive cluster selection — `build_run_plan.py` is the single source of truth
- Scope enforcement separates audit boundaries (`finding_scope_root` vs `context_roots`)

## Vulnerability Categories

Workers specialize in:
- Memory safety (buffer overflows, use-after-free, double-free, format strings)
- Integer arithmetic (overflow, underflow, sign confusion, truncation)
- Race conditions and TOCTOU vulnerabilities
- POSIX API misuse
- Windows-specific attack surfaces
- Injection vulnerabilities (command, path, format string)
