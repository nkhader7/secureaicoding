---
name: constant-time-analysis
description: Detects timing side-channel vulnerabilities in cryptographic implementations across 13 programming languages. Use when auditing code that processes secrets, keys, tokens, or authentication data.
allowed-tools: Bash Read Glob Grep
---

# Constant-Time Analysis

Detects operations that may leak secret data through execution timing variations.

## When to Use

- Auditing cryptographic key operations
- Reviewing authentication token comparison
- Analyzing password verification logic
- Security review of any code processing secrets, keys, or auth tokens

## When NOT to Use

- Non-security-sensitive code (timing variation is acceptable)
- Performance profiling (use profilers instead)

## Supported Languages

**Compiled** (assembly analysis): C, C++, Go, Rust, Swift

**VM-compiled** (bytecode analysis): Java, Kotlin, C#

**Interpreted** (source analysis): PHP, JavaScript, TypeScript, Python, Ruby

## Primary Detection Targets

| Vulnerability | Description |
|---------------|-------------|
| Division on secrets | `DIV`, `IDIV`, `SDIV`, `UDIV` — variable-time CPU instruction |
| Secret-dependent branches | Conditional jumps based on secret values |
| Insecure comparisons | `memcmp`, `==` for secret comparison |
| Weak RNG | Timing-predictable random number generation |
| Secret-dependent table lookups | Array indexed by secret byte |

## Critical Limitation

**The tool has NO data flow analysis.** It flags ALL potentially dangerous operations regardless of whether they involve secrets.

**Required**: Manual verification to trace whether flagged operations actually process sensitive data or operate on public values (lengths, counts, indices).

## Real-World Impact

- **KyberSlash (2023)**: Division timing in post-quantum implementations
- **Lucky Thirteen (2013)**: CBC padding timing attacks on TLS
- **RSA timing**: Key bit leakage through variable-time division

## Language-Specific References

- **Compiled languages (C, C++, Go, Rust)**: See [compiled.md](references/compiled.md)
- **PHP**: See [php.md](references/php.md)
- **JavaScript/TypeScript**: See [javascript.md](references/javascript.md)
- **Python**: See [python.md](references/python.md)
- **Ruby**: See [ruby.md](references/ruby.md)

## Safe Alternatives

| Vulnerable | Safe Alternative |
|-----------|-----------------|
| `memcmp(a, b, len)` | `CRYPTO_memcmp(a, b, len)` (OpenSSL), `subtle.ConstantTimeCompare(a, b)` (Go) |
| `if (secret) { a } else { b }` | `uint32_t mask = -(uint32_t)(secret != 0); (a & mask) \| (b & ~mask)` |
| `a / divisor` (secret divisor) | Barrett reduction |

## Common Mistakes

1. **Testing only one optimization level** — O2 may eliminate the division you're worried about, or introduce one
2. **Testing only one architecture** — ARM and x86 have different division behavior
3. **Ignoring conditional branches** — Use `--warnings` to surface branch analysis
4. **Fixing symptoms not causes** — If compiler introduces division, the algorithm may need redesign
