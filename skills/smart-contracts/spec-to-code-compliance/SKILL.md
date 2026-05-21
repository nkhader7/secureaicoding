---
name: spec-to-code-compliance
description: Verifies blockchain implementations against their specifications. Use when auditing smart contracts or protocols where both documentation and code are available for comparison.
allowed-tools: Read Bash Glob Grep WebFetch
---

# Spec-to-Code Compliance Checker

Systematically validates that code implements exactly what documentation specifies. Particularly valuable for smart contract audits and protocol verification.

## When to Use

- Smart contract audits with available specification documents
- Protocol implementation verification
- When spec diverges from code behavior (found bug or undocumented feature?)
- Pre-audit to understand intended vs. actual behavior

## When NOT to Use

- Code without any specification or documentation
- General code quality review
- Finding vulnerabilities without a spec to compare against

## Seven-Phase Workflow

### Phase 0: Documentation Discovery
Identify ALL documentation sources — specs may appear as:
- Whitepapers (PDF)
- Design notes (Markdown)
- Architecture docs
- Protocol transcripts
- README files with invariants

### Phase 1: Spec Normalization
Convert diverse formats (PDF, Markdown, HTML) into a canonical corpus.
- Preserve structural information (hierarchies, formulas)
- Retain section references for citation

### Phase 2: Spec Intent Extraction (Spec-IR)
Extract intended behavior into a structured IR:
- Protocol purpose and actors
- Variables and state transitions
- Invariants (must always hold)
- Security requirements
- Each item gets a **confidence score**

### Phase 3: Code Behavior Analysis (Code-IR)
Granular line-by-line analysis:
- State changes and their conditions
- Control flow paths
- External calls and their assumptions
- Implicit assumptions not in the spec

### Phase 4: Alignment Comparison
Compare Spec-IR against Code-IR to generate **Alignment Records**:

| Classification | Meaning |
|----------------|---------|
| Full match | Code exactly implements spec |
| Partial match | Code implements most of spec item |
| Mismatch | Code contradicts spec |
| Undocumented behavior | Code behavior not in spec |

### Phase 5: Divergence Categorization

| Severity | Meaning |
|----------|---------|
| Critical | Security-relevant divergence |
| High | Functional divergence with impact |
| Medium | Partial implementation |
| Low | Minor documentation gap |

### Phase 6: Compliance Report
Produces audit-grade report with:
- Findings with severity levels
- Exact citations from spec and code
- Risk assessment
- Remediation guidance

## Critical Principles

- **No inference**: Ambiguities must be classified as ambiguous, not resolved through assumption
- **Evidence required**: Every finding needs exact citations with line numbers
- **Confidence scoring**: Rate confidence in each extracted spec item
- **Undocumented behavior is a finding**: Behavior that exists in code but not spec is noteworthy

## Output: 16-Section Compliance Report

1. Executive summary
2. Scope definition
3. Documentation sources
4. Spec-IR summary
5. Code-IR summary
6. Alignment matrix
7. Critical divergences
8. High divergences
9. Medium divergences
10. Low divergences
11. Undocumented behaviors
12. Spec ambiguities
13. Analysis limitations
14. Recommendations
15. Full alignment records
16. Appendices (raw IR data)
