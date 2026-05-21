---
name: semgrep-rule-variant-creator
description: Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to new target languages or creating language-specific variants of a universal vulnerability pattern.
allowed-tools: Bash Read Write Edit Glob Grep WebFetch
---

# Semgrep Rule Variant Creator

Port existing Semgrep rules to new target languages with applicability analysis and test-driven validation.

## When to Use

- Porting an existing Semgrep rule to one or more new languages
- Creating language-specific variants of a universal vulnerability pattern
- Expanding rule coverage across a polyglot codebase
- Translating rules between languages with equivalent constructs

## When NOT to Use

- Creating a new Semgrep rule from scratch (use `semgrep-rule-creator` instead)
- Running existing rules against code
- Languages where the vulnerability pattern fundamentally doesn't apply

## Inputs Required

1. **Existing Semgrep rule** — YAML file path or YAML content
2. **Target languages** — One or more languages to port to

## Output

For each applicable target language:
```
<original-rule-id>-<language>/
├── <original-rule-id>-<language>.yaml
└── <original-rule-id>-<language>.<ext>
```

## Four-Phase Workflow (Per Language)

Complete the full cycle for each language before starting the next.

### Phase 1: Applicability Analysis

**Verdict options**:
- `APPLICABLE` → Proceed with variant creation
- `APPLICABLE_WITH_ADAPTATION` → Proceed but significant changes needed
- `NOT_APPLICABLE` → Skip with documentation of why

See [applicability-analysis.md](references/applicability-analysis.md) for the full analysis framework.

### Phase 2: Test Creation (Test-First)

Create test file with target language idioms:
- Minimum 2 vulnerable cases (`# ruleid:`)
- Minimum 2 safe cases (`# ok:`)
- Language-specific edge cases

### Phase 3: Rule Creation

```bash
# Analyze AST structure in target language
semgrep --dump-ast -l <lang> test-file
```

Translate patterns to target language syntax:
- Update `languages:` key
- Adapt pattern syntax for language idioms
- Update `message` and `id`

### Phase 4: Validation

```bash
semgrep --validate --config rule.yaml
semgrep --test --config rule.yaml test-file
```

**Checkpoint**: Output MUST show `All tests passed`.

## Rationalizations to Reject

| Rationalization | Why It Fails |
|-----------------|--------------|
| "Pattern structure is identical" | Different ASTs across languages require AST dump |
| "Same vulnerability, same detection" | Data flow patterns differ between languages |
| "Rule doesn't need tests since original worked" | Language edge cases differ |
| "Skip applicability — it obviously applies" | Some patterns are language-specific |
| "Just translate the syntax 1:1" | Languages have different idioms |

## Reference Files

- [applicability-analysis.md](references/applicability-analysis.md) — Framework for deciding if a rule applies
- [language-syntax-guide.md](references/language-syntax-guide.md) — Syntax differences by language
- [workflow.md](references/workflow.md) — Detailed per-phase workflow
