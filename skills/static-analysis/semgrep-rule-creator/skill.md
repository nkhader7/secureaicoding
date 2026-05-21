---
name: semgrep-rule-creator
description: Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rules or building custom static analysis detections.
allowed-tools: Bash Read Write Edit Glob Grep WebFetch
---

# Semgrep Rule Creator

Create production-quality Semgrep rules with proper testing and validation.

## When to Use

**Ideal scenarios:**
- Writing Semgrep rules for specific bug patterns
- Writing rules to detect security vulnerabilities in your codebase
- Writing taint mode rules for data flow vulnerabilities
- Writing rules to enforce coding standards

## When NOT to Use

Do NOT use this skill for:
- Running existing Semgrep rulesets
- General static analysis without custom rules (use `semgrep` skill)

## Rationalizations to Reject

When writing Semgrep rules, reject these common shortcuts:

- **"The pattern looks complete"** → Still run `semgrep --test --config <rule-id>.yaml <rule-id>.<ext>` to verify. Untested rules have hidden false positives/negatives.
- **"It matches the vulnerable case"** → Matching vulnerabilities is half the job. Verify safe cases don't match (false positives break trust).
- **"Taint mode is overkill for this"** → If data flows from user input to a dangerous sink, taint mode gives better precision than pattern matching.
- **"One test is enough"** → Include edge cases: different coding styles, sanitized inputs, safe alternatives, and boundary conditions.
- **"I'll optimize the patterns first"** → Write correct patterns first, optimize after all tests pass. Premature optimization causes regressions.
- **"The AST dump is too complex"** → The AST reveals exactly how Semgrep sees code. Skipping it leads to patterns that miss syntactic variations.

## Anti-Patterns

**Too broad** - matches everything, useless for detection:
```yaml
# BAD: Matches any function call
pattern: $FUNC(...)

# GOOD: Specific dangerous function
pattern: eval(...)
```

**Missing safe cases in tests** - leads to undetected false positives:
```python
# BAD: Only tests vulnerable case
# ruleid: my-rule
dangerous(user_input)

# GOOD: Include safe cases to verify no false positives
# ruleid: my-rule
dangerous(user_input)

# ok: my-rule
dangerous(sanitize(user_input))

# ok: my-rule
dangerous("hardcoded_safe_value")
```

## Strictness Level

This workflow is **strict** - do not skip steps:
- **Read documentation first**: See [Documentation](#documentation) before writing Semgrep rules
- **Test-first is mandatory**: Never write a rule without tests
- **100% test pass is required**: "Most tests pass" is not acceptable
- **Optimization comes last**: Only simplify patterns after all tests pass
- **One YAML file - one Semgrep rule**: Each YAML file must contain only one rule
- **Forbidden `todook` and `todoruleid` annotations**: Future-improvement annotations are forbidden

## Overview

Rules are created iteratively: analyze the problem, write tests first, analyze AST structure, write the rule, iterate until all tests pass, optimize the rule.

**Approach selection:**
- **Taint mode** (prioritize): Data flow issues where untrusted input reaches dangerous sinks
- **Pattern matching**: Simple syntactic patterns without data flow requirements

**Output structure** - exactly 2 files in a directory named after the rule-id:
```
<rule-id>/
├── <rule-id>.yaml     # Semgrep rule
└── <rule-id>.<ext>    # Test file with ruleid/ok annotations
```

## Quick Start

```yaml
rules:
  - id: insecure-eval
    languages: [python]
    severity: HIGH
    message: User input passed to eval() allows code execution
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: eval(...)
```

## Quick Reference

- For commands, pattern operators, and taint mode syntax, see [quick-reference.md](references/quick-reference.md).
- For detailed workflow and examples, see [workflow.md](references/workflow.md).

## Workflow

```
Semgrep Rule Progress:
- [ ] Step 1: Analyze the Problem
- [ ] Step 2: Write Tests First
- [ ] Step 3: Analyze AST structure
- [ ] Step 4: Write the rule
- [ ] Step 5: Iterate until all tests pass (semgrep --test)
- [ ] Step 6: Optimize the rule (remove redundancies, re-test)
- [ ] Step 7: Final Run
```

## Documentation

**REQUIRED**: Before writing any rule, use WebFetch to read all of these Semgrep documentation links:

1. [Rule Syntax](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/rule-syntax.md)
2. [Pattern Syntax](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/pattern-syntax.mdx)
3. [Testing Rules](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/testing-rules.md)
4. [Taint analysis](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/data-flow/taint-mode/overview.md)
5. [Advanced taint analysis](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/data-flow/taint-mode/advanced.md)
6. [Constant propagation](https://raw.githubusercontent.com/semgrep/semgrep-docs/refs/heads/main/docs/writing-rules/data-flow/constant-propagation.md)
7. [Trail of Bits Testing Handbook - Semgrep](https://raw.githubusercontent.com/trailofbits/testing-handbook/refs/heads/main/content/docs/static-analysis/semgrep/10-advanced.md)
