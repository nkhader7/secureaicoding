# Semgrep Rule Quick Reference

## Core Rule Structure

```yaml
rules:
  - id: rule-id
    languages: [python]
    severity: HIGH          # LOW, MEDIUM, HIGH, CRITICAL
    message: Description of the finding
    pattern: dangerous(...)
```

## Pattern Operators

| Operator | Purpose |
|----------|---------|
| `pattern` | Simple match — AND with other operators |
| `patterns` | Logical AND — all must match |
| `pattern-either` | Logical OR — any must match |
| `pattern-not` | Exclusion — must NOT match |
| `pattern-inside` | Match only within this context |
| `pattern-not-inside` | Match only outside this context |
| `focus-metavariable` | Report location of specific metavariable |

## Metavariables

- `$VAR` — matches any expression (must be uppercase)
- `$...ARGS` — matches zero or more arguments
- `...` — ellipsis wildcard (any code)
- `<... pattern ...>` — deep expression match (searches nested expressions)

## Typed Metavariables

```yaml
# C
pattern: (int16_t $X) / $Y

# Java
pattern: (java.util.logging.Logger $LOGGER).info(...)
```

## Taint Mode

```yaml
mode: taint
pattern-sources:
  - pattern: request.args.get(...)
pattern-sinks:
  - pattern: eval(...)
pattern-sanitizers:         # optional
  - pattern: sanitize(...)
```

### Taint Options

```yaml
pattern-sources:
  - pattern: $X
    by-side-effect: true    # $X is tainted after this call
    exact: true             # only $X is tainted, not return value
```

## Test File Annotations

```python
# ruleid: my-rule          # Next line MUST match
dangerous_func(user_input)

# ok: my-rule              # Next line must NOT match
safe_func(user_input)
```

**CRITICAL**: Comment must be on the line IMMEDIATELY BEFORE the code.

## Debugging Commands

```bash
# Dump AST to understand code structure
semgrep --dump-ast --lang python code.py

# Debug taint flow
semgrep --dataflow-traces --config rule.yaml test.py

# Validate YAML
semgrep --validate --config rule.yaml

# Run tests
semgrep --test --config rule.yaml test.py
```

## Metavariable Filters

```yaml
patterns:
  - pattern: $FUNC(...)
  - metavariable-regex:
      metavariable: $FUNC
      regex: ^(eval|exec|compile)$
  - metavariable-comparison:
      metavariable: $N
      comparison: $N > 0
  - metavariable-type:
      metavariable: $X
      types: [str, bytes]
```

## Common Pattern Equivalences

| Written | Also Matches |
|---------|-------------|
| `func(...)` | `func()`, `func(a)`, `func(a,b)` |
| `"string"` | `'string'` (language-dependent) |
| `func($X, ...)` | `func($X)`, `func($X, a, b)` |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Rule matches nothing | Pattern too specific | Use `--dump-ast` to check structure |
| Too many false positives | Pattern too broad | Add `pattern-not` exclusions |
| Taint not propagating | Missing source/sink | Use `--dataflow-traces` |
| YAML error | Indentation issue | Run `--validate` first |
| Wrong line reported | Need focus | Add `focus-metavariable` |
