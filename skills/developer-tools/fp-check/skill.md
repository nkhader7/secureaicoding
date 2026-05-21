---
name: fp-check
description: Verifies whether security findings are genuine vulnerabilities or false positives before reporting. Use when triaging security tool output or before filing security findings.
allowed-tools: Bash Read Glob Grep
---

# False Positive Check

Verifies whether security findings are genuine vulnerabilities or false positives before reporting.

## When to Use

- Triaging output from security scanners (Semgrep, CodeQL, Bandit, etc.)
- Before reporting findings to developers or filing issues
- When a finding seems suspicious or hard to exploit
- Quality control on security audit findings

## Verification Levels

### Standard Verification
Quick triage for most findings:

1. **Reproduce the finding**: Confirm the pattern actually exists at the reported location
2. **Trace data flow**: Does untrusted data actually reach the sink?
3. **Check context**: Is this in test code, dead code, or unreachable paths?
4. **Verify exploitability**: Can the condition actually occur in production?

### Deep Verification
For high-severity or complex findings:

1. Build a minimal reproduction case
2. Verify all preconditions can be satisfied simultaneously
3. Check for sanitization between source and sink
4. Confirm the vulnerability has real security impact

## Reference Files

- [standard-verification.md](references/standard-verification.md) — Quick triage workflow
- [deep-verification.md](references/deep-verification.md) — Thorough verification for complex findings
- [false-positive-patterns.md](references/false-positive-patterns.md) — Common FP patterns by vulnerability class
- [bug-class-verification.md](references/bug-class-verification.md) — Verification checklist by bug class
- [gate-reviews.md](references/gate-reviews.md) — Quality gates before reporting
- [evidence-templates.md](references/evidence-templates.md) — Templates for documenting evidence

## Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **Confirmed** | Exploitation verified or evidence is definitive | Report |
| **Likely** | Strong evidence, exploitation plausible | Report with caveat |
| **Uncertain** | Evidence is ambiguous | Deep verification required |
| **False Positive** | Finding is definitely wrong | Discard with explanation |

## Common False Positive Patterns

- **Test code**: Vulnerability pattern in test fixtures (intentionally insecure)
- **Dead code**: Unreachable through any code path
- **Input already validated**: Sanitization between source and sink
- **Non-secret data**: Flagged variable contains non-sensitive values
- **Framework guarantee**: Framework handles the issue transparently
- **Safe algorithm in context**: Weak crypto used only for non-security checksums

## Gate Review Checklist

Before reporting any finding:

- [ ] Location confirmed (file + line number verified)
- [ ] Data flow traced (source → transformation → sink)
- [ ] Context checked (not test/dead/generated code)
- [ ] Exploitability assessed (conditions can be satisfied)
- [ ] Impact documented (what does successful exploitation achieve?)
- [ ] Evidence attached (code snippet, trace, or reproduction)
