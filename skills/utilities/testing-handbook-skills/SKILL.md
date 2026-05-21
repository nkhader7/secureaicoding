---
name: testing-handbook-skills
description: Security testing skills derived from the Trail of Bits Testing Handbook, covering fuzzing, coverage analysis, sanitizers, and security testing methodologies.
allowed-tools: Bash Read Write Edit Glob Grep WebFetch
---

# Testing Handbook Skills

A collection of security testing skills derived from the [Trail of Bits Testing Handbook](https://appsec.guide/), covering fuzzing, coverage analysis, sanitizers, and testing methodology.

## Available Sub-Skills

### Fuzzing Frameworks
- **libfuzzer** — LLVM's built-in fuzzer for C/C++
- **aflpp** — AFL++ advanced fuzzing for C/C++
- **cargo-fuzz** — Fuzzing for Rust with libFuzzer
- **libafl** — LibAFL (Rust-based fuzzing framework)
- **atheris** — Python fuzzing with libFuzzer
- **ruzzy** — Ruby fuzzing

### Harness Writing
- **harness-writing** — Writing effective fuzzing harnesses that maximize coverage and minimize false positives

### Coverage and Analysis
- **coverage-analysis** — Analyzing code coverage to identify fuzzing blind spots
- **fuzzing-dictionary** — Building fuzzing dictionaries from known patterns
- **fuzzing-obstacles** — Overcoming checksums, magic bytes, and other fuzzing obstacles

### Sanitizers
- **address-sanitizer** — Using AddressSanitizer (ASan) to detect memory errors

### Specialized Testing
- **constant-time-testing** — Testing for timing side-channels
- **wycheproof** — Testing cryptographic implementations with Project Wycheproof

### Testing Generator
- **testing-handbook-generator** — Generates customized testing guidance from the Testing Handbook for a specific project

## Quick Reference by Goal

| Goal | Sub-Skill |
|------|-----------|
| Fuzz a C/C++ library | libfuzzer or aflpp |
| Fuzz a Rust library | cargo-fuzz or libafl |
| Fuzz a Python project | atheris |
| Write a fuzzing harness | harness-writing |
| Analyze coverage gaps | coverage-analysis |
| Detect memory bugs | address-sanitizer |
| Test crypto implementations | wycheproof |
| Detect timing issues | constant-time-testing |
| Get project-specific guidance | testing-handbook-generator |

## Testing Handbook Resources

Full documentation available at [appsec.guide](https://appsec.guide/docs/).
