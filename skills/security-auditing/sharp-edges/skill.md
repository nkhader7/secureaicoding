---
name: sharp-edges
description: Identifies security design patterns in APIs, configurations, and interfaces that enable developer misuse. Use during API design reviews or when analyzing why a vulnerability was easy to introduce.
allowed-tools: Read Bash Grep Glob
---

# Sharp Edges Analysis

Identifies designs where insecure usage is easier than secure usage — violations of the **pit of success** principle.

## When to Use

- API design review (new or existing)
- Post-mortem analysis of how a vulnerability was introduced
- Cryptographic library evaluation
- Security configuration schema review
- SDK or framework security assessment

## When NOT to Use

- General code review (use `differential-review` skill)
- Finding specific CVEs (use `static-analysis` skills)

## Core Principle

> "If developers must understand cryptography, read documentation carefully, or remember special rules to avoid vulnerabilities, the API has failed."

Secure usage must be the **default** or **only** option. Documentation cannot substitute for safe design.

## Six Footgun Categories

### 1. Algorithm/Mode Selection
APIs that accept algorithm parameters let developers choose weak options.

```python
# FOOTGUN: Lets developer choose weak algorithm
jwt.encode(payload, secret, algorithm=algorithm)  # algorithm="none" bypasses verification

# SAFE: Algorithm is fixed
jwt.encode_hs256(payload, secret)  # No choice = no misuse
```

### 2. Dangerous Defaults
Zero, empty, or null values that disable security or have ambiguous meaning.

```python
# FOOTGUN: lifetime=0 could mean infinite or instant expiry
create_token(payload, lifetime=0)

# FOOTGUN: Empty string disables auth
connect(password="")
```

### 3. Primitive vs. Semantic APIs
Raw bytes instead of typed security concepts enable parameter swapping.

```python
# FOOTGUN: Two byte arrays — easy to swap nonce and key
encrypt(key: bytes, nonce: bytes, plaintext: bytes)

# SAFE: Named types prevent confusion
encrypt(key: EncryptionKey, nonce: Nonce, plaintext: Plaintext)
```

### 4. Configuration Cliffs
A single misconfigured setting causes catastrophic failure with no warning.

```python
# FOOTGUN: One wrong option disables TLS verification silently
requests.get(url, verify=False)

# FOOTGUN: Missing required config allows insecure fallback
ssl_context = ssl.SSLContext()  # Insecure defaults if not hardened
```

### 5. Silent Failures
Security operations that fail quietly or return booleans instead of raising errors.

```python
# FOOTGUN: Returns False on auth failure, easy to ignore
if auth.verify(token):
    pass

# SAFE: Raises exception on failure — cannot be silently ignored
auth.require_valid(token)  # raises AuthError
```

### 6. Stringly-Typed Security
Security-critical values as plain strings invite injection and confusion.

```python
# FOOTGUN: Permission name as string — typos silently pass
require_permission("admin ")  # trailing space bypasses check

# SAFE: Enum prevents injection and typos
require_permission(Permission.ADMIN)
```

## Analysis Workflow

1. **Surface Identification**: Map all security APIs, developer choice points, configuration schemas
2. **Edge Case Probing**: Test behaviors with zero, empty, null, negative values and type mismatches
3. **Threat Modeling**: Consider scenarios from:
   - Malicious users (what can they control?)
   - Lazy developers (what's the path of least resistance?)
   - Confused developers (what looks right but is wrong?)
4. **Validate Findings**: Reproduce misuse cases and verify exploitability

## Rationalizations to Reject

- **"It's documented"** → Documentation doesn't prevent misuse; design must
- **"Developers should know better"** → API must make correct usage obvious
- **"Nobody would do that"** → Someone will, especially under deadline pressure
- **"Advanced users need flexibility"** → Flexibility and safety aren't mutually exclusive
- **"It's backwards compatible"** → Breaking changes are acceptable for security
