# The Philosophy of Generic but Precise Variant Analysis

## Why Variants Exist

Vulnerabilities cluster because developers make consistent mistakes:

1. **Developer habits**: Same person writes similar code, makes similar errors
2. **Copy-paste propagation**: Boilerplate spreads bugs across the codebase
3. **API misuse patterns**: Complex APIs invite consistent misunderstandings
4. **Framework idioms**: Framework patterns create predictable vulnerability shapes
5. **Incomplete fixes**: Original bug fixed in one place, missed elsewhere

## Root Cause Analysis

Before searching, extract the essential vulnerability pattern:

### Ask These Questions

1. **What operation is dangerous?** (e.g., `eval()`, `system()`, raw SQL)
2. **What data makes it dangerous?** (e.g., user-controlled input)
3. **What's missing?** (e.g., sanitization, validation, bounds check)
4. **What context enables it?** (e.g., authentication state, error handling path)

### The Root Cause Statement

Formulate a clear statement:

> "This vulnerability exists because [UNTRUSTED DATA] reaches [DANGEROUS OPERATION] without [REQUIRED PROTECTION]."

Examples:
- "User input reaches `eval()` without sanitization"
- "Attacker-controlled size reaches `malloc()` without overflow check"
- "Untrusted path reaches `open()` without canonicalization"

This statement IS your search pattern.

## The Abstraction Ladder

### Level 0: Exact Match

Match the literal vulnerable code:

```python
# Original vulnerable code
query = "SELECT * FROM users WHERE id=" + request.args.get('id')
```

```bash
rg 'SELECT \* FROM users WHERE id=" \+ request\.args\.get'
```

- **Matches**: 1 (the original)
- **False positives**: 0
- **Value**: Confirms the bug exists, baseline for generalization

### Level 1: Variable Abstraction

Replace variable names with wildcards:

```yaml
pattern: $QUERY = "SELECT * FROM users WHERE id=" + $INPUT
```

- **Matches**: 3-5 (same query pattern, different variables)
- **Value**: Find copy-paste variants

### Level 2: Structural Abstraction

Generalize the structure:

```yaml
patterns:
  - pattern: $Q = "..." + $INPUT
  - pattern-inside: |
      def $FUNC(...):
        ...
        cursor.execute($Q)
```

- **Matches**: 10-30 (any string concat used in query)
- **Value**: Find pattern variants

### Level 3: Semantic Abstraction

Abstract to the security property:

```yaml
mode: taint
pattern-sources:
  - pattern: request.args.get(...)
  - pattern: request.form.get(...)
pattern-sinks:
  - pattern: cursor.execute(...)
```

- **Matches**: 50-100+ (any user input to any query)
- **Value**: Comprehensive coverage, requires triage

### Choosing Your Level

| Goal | Recommended Level |
|------|-------------------|
| Verify a specific fix | Level 0 |
| Find copy-paste bugs | Level 1 |
| Audit a component | Level 2 |
| Full security assessment | Level 3 |

## The Generalization Process

### Rule: One Change at a Time

Never generalize multiple elements simultaneously:

```
BAD:  exact code → fully abstract pattern
GOOD: exact code → abstract var1 → abstract var2 → abstract operation
```

Each step:
1. Make ONE change
2. Run the pattern
3. Review ALL new matches
4. Decide: acceptable FP rate?
5. Continue or revert

## False Positive Management

### Acceptable FP Rates by Context

| Context | Acceptable FP Rate |
|---------|-------------------|
| Automated CI blocking | <5% |
| Developer warning | <20% |
| Security audit triage | <50% |
| Research/exploration | <80% |

### Common FP Filters

**Dead code**:
```yaml
pattern-not-inside: |
  if False:
    ...
```

**Test code**:
```bash
rg "pattern" --glob '!**/test*' --glob '!**/*_test.*'
```

**Already sanitized**:
```yaml
pattern-not: dangerous_func(sanitize($X))
```

## Expanding Vulnerability Classes

For each root cause, systematically expand to related classes:

1. **What other attributes/functions have similar semantics?**
   - If bug involves `isAuthenticated`, also check: `isActive`, `isAdmin`, `isVerified`

2. **What other boolean logic errors could occur?**
   - Inverted conditions (`if not x` vs `if x`)
   - Wrong default return value (`return true` vs `return false`)

3. **What edge cases exist for the data types involved?**
   - Null/None/undefined comparisons
   - Empty string vs null
   - Zero vs null
   - Empty array/collection

4. **What documentation mismatches could exist?**
   - Function name suggests one behavior, code does another

### Null Equality Bypasses

```python
# If anonymous_user.id is None and guest_order.owner_id is None
# Then None == None evaluates to True, bypassing the check
if order.owner_id == current_user.id:
    return True  # BUG: Allows access to anonymous users
```

## Tracking Your Hunt

Maintain a tracking document:

```markdown
## Variant Analysis: [Original Bug ID]

### Root Cause
[Statement of the vulnerability pattern]

### Patterns Tried
| Pattern | Level | Matches | True Pos | False Pos | Notes |
|---------|-------|---------|----------|-----------|-------|
| exact   | 0     | 1       | 1        | 0         | Baseline |

### Confirmed Variants
| Location | Severity | Status | Notes |
|----------|----------|--------|-------|

### False Positive Patterns
- Pattern X: Always FP because [reason]
```

## Anti-Patterns to Avoid

1. **Starting Too Generic**: Jump straight to semantic analysis instead of exact match
2. **Generalizing Everything**: Abstract all elements at once instead of one at a time
3. **Ignoring False Positives**: "I'll triage later" instead of analyzing FPs immediately
4. **Tool Loyalty**: Only using CodeQL instead of ripgrep for recon, Semgrep for iteration
5. **Pattern Hoarding**: Keeping patterns with high FP rates

## Summary: The Expert Mindset

1. **Understand before searching**: Root cause analysis is non-negotiable
2. **Start specific**: First pattern should match exactly one thing
3. **Climb the ladder**: Generalize one step at a time
4. **Measure as you go**: Track matches and FP rates at each step
5. **Know when to stop**: High FP rate means you've gone too far
6. **Expand vulnerability classes**: One root cause has many manifestations
7. **Check semantics**: Verify code matches documentation intent
8. **Test edge cases**: Null values and boundary conditions reveal hidden bugs
