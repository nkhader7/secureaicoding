---
name: semgrep
description: Executes Semgrep security scans against codebases with parallel language detection. Use when running existing Semgrep rulesets for comprehensive security scanning.
allowed-tools: Bash Read Write Glob Grep
---

# Semgrep Security Scanner

Executes static analysis on codebases using Semgrep with parallel execution and automated language detection.

## When to Use

- Running security scans against a codebase
- Applying existing Semgrep rulesets (Trail of Bits, 0xdea, Decurity)
- Continuous security scanning in CI/CD
- Getting a comprehensive security scan before a code review

## When NOT to Use

- Writing new Semgrep rules (use `semgrep-rule-creator` skill)
- Languages not supported by Semgrep

## Core Workflow

1. **Language detection**: Determine target languages, check Semgrep Pro availability
2. **Scan mode selection**: Comprehensive coverage vs. security-focused scanning
3. **Plan approval (hard gate)**: Present exact rulesets and await explicit user consent
4. **Parallel task spawning**: Launch scanner subagents concurrently per language
5. **Results merging**: Consolidate SARIF output and summarize findings

## Critical Requirements

**Telemetry prevention**: Every Semgrep command MUST include `--metrics=off`.

**User approval is mandatory**: The initial scan request does NOT constitute approval. Present exact rulesets, target directories, execution mode, then await explicit confirmation.

**Third-party rulesets are non-optional**: Include Trail of Bits, 0xdea, and Decurity rulesets when detected languages match.

**Pro availability check**: Verify Pro status before scanning. Cross-file taint analysis catches ~250% more true positives.

**Parallel spawning**: All scan tasks must be created in a single response.

## Output Structure

```
$OUTPUT_DIR/
├── raw/                    # Per-language Semgrep output
│   ├── python.sarif
│   ├── javascript.sarif
│   └── ...
├── results/
│   └── results.sarif       # Merged SARIF
└── rulesets.txt            # Approved rulesets log
```

## Semgrep Command Template

```bash
semgrep scan \
  --metrics=off \
  --config p/security-audit \
  --config p/trailofbits \
  --sarif \
  --output $OUTPUT_DIR/raw/<language>.sarif \
  <target-directory>
```
