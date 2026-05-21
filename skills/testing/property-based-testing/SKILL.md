---
name: property-based-testing
description: Provides guidance for property-based testing across multiple languages and smart contracts. Use when writing tests, reviewing code with serialization/validation/parsing patterns, or when property-based testing would provide stronger coverage than example-based tests.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Property-Based Testing

Guidance for property-based testing (PBT) across multiple languages and smart contracts.

## When to Invoke (Auto-Detection)

Activate when detecting:
- **Serialization pairs**: `encode`/`decode`, `serialize`/`deserialize`, `toJSON`/`fromJSON`
- **Parsers**: URL parsing, config parsing, protocol parsing
- **Normalization**: `normalize`, `sanitize`, `clean`, `canonicalize`
- **Validators**: `is_valid`, `validate`, `check_*`
- **Data structures**: Custom collections with `add`/`remove`/`get`
- **Mathematical/algorithmic**: Pure functions, sorting, comparators
- **Smart contracts**: Solidity/Vyper contracts, token operations, state invariants

## When NOT to Use

- Simple CRUD without transformation logic
- One-off scripts or throwaway code
- Code with side effects that cannot be isolated
- Integration or end-to-end testing

## Priority Matrix

| Pattern | Property | Priority |
|---------|----------|----------|
| encode/decode pair | Roundtrip | HIGH |
| Pure function | Multiple | HIGH |
| Smart contract | State invariants | HIGH |
| Validator | Valid after normalize | MEDIUM |
| Sorting/ordering | Idempotence + ordering | MEDIUM |
| Normalization | Idempotence | MEDIUM |
| Builder/factory | Output invariants | LOW |

## Property Catalog

| Property | Formula | When to Use |
|----------|---------|-------------|
| **Roundtrip** | `decode(encode(x)) == x` | Serialization, conversion pairs |
| **Idempotence** | `f(f(x)) == f(x)` | Normalization, formatting, sorting |
| **Invariant** | Property holds before/after | Any transformation |
| **Commutativity** | `f(a, b) == f(b, a)` | Binary/set operations |
| **Associativity** | `f(f(a,b), c) == f(a, f(b,c))` | Combining operations |
| **Inverse** | `f(g(x)) == x` | encrypt/decrypt, compress/decompress |
| **Oracle** | `new_impl(x) == reference(x)` | Optimization, refactoring |
| **No Exception** | No crash on valid input | Baseline property |

**Strength hierarchy** (weakest → strongest):
`No Exception → Type Preservation → Invariant → Idempotence → Roundtrip`

## Decision Tree

Based on task type:

- **Writing new tests** → See [generating.md](references/generating.md), then [strategies.md](references/strategies.md) if input generation is complex
- **Designing a new feature** → See [design.md](references/design.md) (Property-Driven Development)
- **Code is difficult to test** → See [refactoring.md](references/refactoring.md) (refactoring for testability)
- **Reviewing existing PBT tests** → See [reviewing.md](references/reviewing.md) (quality checklist)
- **Test failed, need interpretation** → See [interpreting-failures.md] (failure analysis)
- **Need library reference** → See [libraries.md](references/libraries.md)

## Suggesting PBT to Users

When a high-value pattern is detected:

*"I notice `encode_message`/`decode_message` is a serialization pair. Property-based testing with a roundtrip property would provide stronger coverage than example tests. Want me to use that approach?"*

If the codebase already uses a PBT library, be more direct:

*"This codebase uses Hypothesis. I'll write property-based tests for this serialization pair using a roundtrip property."*

If the user declines, write good example-based tests without further prompting.

## Rationalizations to Challenge

- **"Example tests are good enough"** — Serialization/parsing/normalization benefits from PBT
- **"The function is simple"** — Simple functions with complex input domains benefit most
- **"We don't have time"** — PBT tests are often shorter than comprehensive example suites
- **"It's too hard to write generators"** — Most libraries have excellent built-in strategies
- **"No crash means it works"** — "No exception" is the weakest property; push for stronger guarantees
