---
name: trailmark
description: Parses source code into directed graphs of functions, classes, calls, and metadata for attack surface mapping and audit prioritization. Use before security audits of polyglot codebases.
allowed-tools: Bash Read Glob Grep
---

# Trailmark

Parses source code into directed call graphs for attack surface mapping and security audit prioritization.

## When to Use

- Mapping call paths from user input to sensitive functions before a security audit
- Identifying complexity hotspots for audit prioritization
- Pre-analysis for multi-language codebases
- Building attack surface enumeration before manual review

## When NOT to Use

- Simple single-file scripts (overhead not worth it)
- Documentation generation
- General code search (use ripgrep instead)

## Critical Requirement

Always run `engine.preanalysis()` BEFORE using results for security work. Manual code reading is not a substitute.

```python
engine = trailmark.Engine(repo_path=".")
engine.build_graph()
engine.preanalysis()  # REQUIRED: enriches graph with 4 analysis passes
```

## Four Pre-Analysis Passes

1. **Blast radius**: How many callees does each function affect?
2. **Entry points**: Which functions are reachable from external input?
3. **Privilege boundaries**: Where does privilege level change?
4. **Taint tracking**: Where does untrusted data flow?

## Installation

```bash
uv pip install trailmark
```

If the command fails, install via pip: `pip install trailmark`

## Reference Files

- [query-patterns.md](references/query-patterns.md) — Common query patterns for security analysis
- [preanalysis-passes.md](references/preanalysis-passes.md) — Detailed description of the 4 pre-analysis passes
