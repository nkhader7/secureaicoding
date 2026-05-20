# Semgrep Rule Creation Workflow

Detailed workflow for creating production-quality Semgrep rules.

## Step 1: Analyze the Problem

Before writing any code:

1. **Fetch external documentation**: See [Documentation](../skill.md#documentation) for required reading
2. **Understand the exact bug pattern**: What vulnerability, issue or pattern should be detected?
3. **Identify the target language**: What is specific about the bug and that language?
4. **Determine the approach**:
   - **Pattern matching**: Syntactic patterns without data flow
   - **Taint mode**: Data flows from untrusted source to dangerous sink

### When to Use Taint Mode

Taint mode tracks the flow of data from one location to another:

- **Track data flow across multiple variables**: Trace how data moves and identify insecure flow paths
- **Find injection vulnerabilities**: SQL injection, command injection, XSS
- **Write simple and resilient rules**: Handles nested if statements, loops, and other structures

## Step 2: Write Tests First

**Why test-first?** Writing tests before the rule forces you to think about both vulnerable AND safe cases.

Create directory and test file with annotations (`# ruleid:`, `# ok:` only).

### Directory Structure

```
<rule-id>/
├── <rule-id>.yaml     # Semgrep rule
└── <rule-id>.<ext>    # Test file with ruleid/ok annotations
```

**CRITICAL**:
1. The comment must be on the line IMMEDIATELY BEFORE the code.
2. The comment must contain ONLY the comment marker and annotation.

### Test Case Design

Include test cases for:
- Clear vulnerable cases (must match)
- Clear safe cases (must not match)
- Edge cases and variations
- Different coding styles
- Sanitized/validated input (must not match)
- Nested structures (inside if statements, loops, try/catch blocks)

## Step 3: Analyze AST Structure

**Why analyze AST?** Semgrep matches against the AST, not raw text.

```bash
semgrep --dump-ast --lang <language> <rule-id>.<ext>
```

## Step 4: Write the Rule

Choose appropriate pattern operators and write the rule.

### Validate and Test

```bash
# Validate YAML syntax
semgrep --validate --config <rule-id>.yaml

# Run tests
cd <rule-directory>
semgrep --test --config <rule-id>.yaml <rule-id>.<ext>
```

Expected output: `1/1: ✓ All tests passed`

### Debug Taint Mode Rules

```bash
semgrep --dataflow-traces --config <rule-id>.yaml <rule-id>.<ext>
```

## Step 5: Iterate Until Tests Pass

Each time you introduce changes, test the rule:

```bash
semgrep --test --config <rule-id>.yaml <rule-id>.<ext>
```

**Verification checkpoint**: Output MUST show "All tests passed".

### Common Fixes

| Problem | Solution |
|---------|----------|
| Too many matches | Add `pattern-not` exclusions |
| Missing matches | Add `pattern-either` variants |
| Wrong line matched | Adjust `focus-metavariable` |
| Taint not flowing | Check sanitizers aren't too broad |
| Taint false positive | Add sanitizer pattern |

## Step 6: Optimize the Rule

After all tests pass, remove redundant patterns.

### Common Redundancies to Remove

**Quote Variants** (language-dependent):
```yaml
# Before
pattern-either:
  - pattern: hashlib.new("md5", ...)
  - pattern: hashlib.new('md5', ...)
# After
pattern-either:
  - pattern: hashlib.new("md5", ...)
```

**Ellipsis Subsets**:
```yaml
# Before
pattern-either:
  - pattern: dangerous($X, ...)
  - pattern: dangerous($X)
  - pattern: dangerous($X, $Y)
# After
pattern: dangerous($X, ...)
```

**Consolidate with Metavariables**:
```yaml
# Before
pattern-either:
  - pattern: md5($X)
  - pattern: sha1($X)
# After
patterns:
  - pattern: $FUNC($X)
  - metavariable-regex:
      metavariable: $FUNC
      regex: ^(md5|sha1)$
```

**CRITICAL**: Always re-run tests after optimization.

## Step 7: Final Run

Run the Semgrep rule: `semgrep --config <rule-id>.yaml <rule-id>.<ext>`

Ensure the message:
1. Contains a short and concise explanation
2. Has no uninterpolated metavariables (e.g., `$OP`, `$VAR`)
