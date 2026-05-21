---
name: differential-review
description: Risk-first security review of PRs, commits, and diffs. Use when reviewing code changes for security implications, especially in authentication, cryptography, and value transfer.
allowed-tools: Bash Read Glob Grep
---

# Differential Security Review

Risk-first, evidence-based security review of code changes with adaptive depth scaling.

## When to Use

- Security review of pull requests
- Pre-merge review of sensitive changes
- Analyzing commits that touch security-critical code
- Post-incident analysis of a change that introduced a vulnerability

## Risk Classification

**HIGH** — requires exhaustive analysis:
- Authentication/authorization logic changes
- Cryptographic operations
- External API calls or network communication
- Value transfers (payments, tokens, balances)
- Input validation/sanitization changes

**MEDIUM** — requires focused analysis:
- Business logic changes
- State management

**LOW** — quick review:
- Comments, documentation
- Tests (unless they reveal intent)
- UI changes without security implications

## Adaptive Scope Strategy

| Codebase Size | Approach |
|---------------|---------|
| Small (<20 files) | Exhaustive — complete dependency tracing |
| Medium (20–200 files) | Focused — priority areas only |
| Large (200+ files) | Surgical — critical paths only |

## Six-Phase Workflow

1. **Initial Triage**: Classify changes by risk level, identify blast radius
2. **Code Analysis**: Line-by-line review of HIGH-risk changes
3. **Test Coverage**: Evaluate whether security cases are tested
4. **Blast Radius**: Calculate how many callers are affected by changes
5. **Deep Investigation**: Trace data flow, check auth enforcement, verify crypto
6. **Adversarial Modeling**: "How would an attacker exploit this change?"

## Red Flags (Escalation Triggers)

Immediately investigate:
- Removal of security-related code (auth checks, validation, crypto)
- Access control modifier changes (`private` → `public`, role changes)
- Validation logic elimination
- New external calls without error handling or input validation
- High blast-radius changes affecting 50+ callers

## Core Principles

- **Risk first**: Spend time proportional to risk level
- **Evidence required**: All findings require file path + line number
- **Git history matters**: Check if the change was intentional or accidental
- **Transparency**: Document what was NOT analyzed

## Output Format

```markdown
## Security Review: [PR/Commit ID]

### Risk Summary
- HIGH risk changes: N
- MEDIUM risk changes: N
- Scope: X files, Y functions

### Findings
| Severity | Location | Finding |
|----------|----------|---------|

### Not Analyzed
- [what was out of scope and why]
```
