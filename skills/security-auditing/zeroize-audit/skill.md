---
name: zeroize-audit
description: Detects missing or ineffective zeroization of sensitive data in C/C++ and Rust codebases. Use when auditing cryptographic code, key management, or any code that handles secrets.
allowed-tools: Bash Read Glob Grep
---

# Zeroize Audit

Detects missing or ineffective zeroization of sensitive data through multi-layer analysis: source code, compiler IR, and assembly verification.

## When to Use

- Auditing cryptographic key lifecycle (generation, use, cleanup)
- Reviewing password handling code
- Analyzing token and session secret management
- Security audits of C, C++, or Rust codebases with sensitive data
- Verifying compiler optimizations don't eliminate security-critical wipes

## Supported Languages

C, C++, Rust

## Approved Zeroization APIs

| Language | Approved API |
|----------|-------------|
| C/C++ | `explicit_bzero`, `memset_s`, `SecureZeroMemory`, `OPENSSL_cleanse`, `sodium_memzero`, volatile wipe loops |
| Rust | `zeroize::Zeroize` trait, `Zeroizing<T>` wrapper, `ZeroizeOnDrop` macro |

**NOT approved**: `memset()` — can be optimized away by dead-store elimination.

## Three Critical Vulnerability Classes

1. **Source-level issues**: Missing zeroization calls, incomplete wipes, unprotected data copies
2. **Compiler optimizations**: Zeroization code eliminated by dead-store elimination (DSE)
3. **Runtime artifacts**: Secrets remaining in stack frames or CPU registers after return

## Detection Methodology

See [detection-strategy.md](references/detection-strategy.md) for the complete 12-step workflow.

**Phase 1: Source-Level Analysis (Steps 1–6)**
- Mandatory preflight check: compile database + compilability
- Identify sensitive objects at three confidence levels:
  - Low: name patterns (`key`, `secret`, `seed`, `token`)
  - Medium: type hints (byte buffers, arrays)
  - High: explicit annotations (`#[secret]`, `__attribute__((annotate("sensitive")))`)
- Check for approved wipe APIs
- MCP semantic pass to resolve symbols and trace cleanup paths
- Validate correctness: wipe size, exit path coverage, ordering before `free()`

**Phase 2: Compiler-Level Analysis (Steps 7–12)**
- IR comparison: detect zeroization optimized away (O0 vs O1 vs O2)
- Assembly analysis: register spills, stack retention
- CFG analysis: wipe operations on ALL exit paths
- PoC generation: proof-of-concept demonstrating exploitability

## Confidence Requirements

| Evidence Level | Status |
|----------------|--------|
| Source pattern only | `needs_review` |
| Single signal | `likely` |
| 2+ independent signals | `confirmed` |

Hard evidence (compiler IR elimination, assembly artifacts) cannot be waived.

## Prerequisites

- C/C++: valid `compile_commands.json`
- Rust: buildable `Cargo.toml`

## Output

Structured JSON findings + human-readable markdown report.

## Rationalizations to Reject

- **"The compiler won't optimize this away"** → Verify with IR diff, don't assume
- **"Performance matters more here"** → Secrets in memory are exploitable; no exception
- **"The data is only held briefly"** → Brief exposure is still exploitable
- **"We'll fix it later"** → Memory forensics, crash dumps, and cold-boot attacks wait for no one
