---
name: entry-point-analyzer
description: Maps all state-changing externally callable functions in smart contract codebases. Use at the start of a smart contract security audit to enumerate the attack surface.
allowed-tools: Bash Read Glob Grep
---

# Entry Point Analyzer

Systematically maps the attack surface of smart contracts by detecting all state-changing externally callable functions and categorizing them by access level.

## When to Use

- Beginning a smart contract security audit
- Mapping attack surface before vulnerability hunting
- Analyzing access control patterns
- Identifying privileged operations

## When NOT to Use

- Vulnerability detection (this maps the surface, not bugs)
- Exploit writing
- Code quality analysis

## Supported Languages

| Language | File Extension |
|----------|----------------|
| Solidity | `.sol` |
| Vyper | `.vy` |
| Solana/Rust | `.rs` |
| Move (Sui/Aptos) | `.move` |
| TON (FunC/Tact) | `.fc`, `.tact` |
| CosmWasm | `.rs` |

## Core Principle

Read-only functions (`view`, `pure`, and equivalents) are **excluded** — they cannot directly cause loss of funds or state corruption.

## Access Classification

| Category | Description |
|----------|-------------|
| **Public (Unrestricted)** | Callable by anyone, no role check |
| **Role-Restricted** | Limited to specific roles (admin, owner, guardian, governance) |
| **Restricted (Review Required)** | Dynamic or ambiguous access control — requires manual verification |
| **Contract-Only** | Callbacks, only callable by other contracts |

## Workflow

1. Detect contract language from file extensions
2. Check for Slither availability (Solidity only — use if available)
3. Locate all contract files in scope
4. Extract state-changing entry points per file
5. Classify by access level
6. Generate structured markdown report

## Output Format

```markdown
## Entry Point Analysis

### Summary
| Access Level | Count |
|--------------|-------|
| Public | N |
| Role-Restricted | N |
| Restricted (Review Required) | N |
| Contract-Only | N |

### Public Functions (Unrestricted)
| Function | Contract | File | Notes |
|----------|----------|------|-------|

### Role-Restricted Functions
| Function | Contract | Role | File |
|----------|----------|------|------|

### Restricted Functions (Manual Review Required)
| Function | Contract | Pattern | File |
|----------|----------|---------|------|

### File Inventory
[List of all analyzed files]

### Analysis Warnings
[Any files or patterns that couldn't be analyzed automatically]
```
