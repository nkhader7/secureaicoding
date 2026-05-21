---
name: audit-context-building
description: Systematically builds deep code understanding before beginning a security audit. Use before vulnerability hunting, threat modeling, or any security analysis that requires thorough code comprehension.
allowed-tools: Read Bash Grep Glob
---

# Audit Context Builder

Performs deep, line-by-line code understanding BEFORE the vulnerability-hunting phase. Reduces hallucinations and missed vulnerabilities by building a complete mental model first.

## When to Use

- Before beginning a security audit or vulnerability hunt
- When deep code comprehension is needed before finding bugs
- Before threat modeling or architecture review
- When reducing hallucinations and context loss is critical

## When NOT to Use

- This skill does NOT produce vulnerability findings
- This skill does NOT recommend fixes
- This skill does NOT assign severity

## Three-Phase Process

### Phase 1: Initial Orientation (Bottom-Up Scan)

1. Identify major modules, files, and contracts
2. Note obvious public/external entrypoints
3. Identify likely actors (users, admins, contracts)
4. Identify important storage variables and state structs
5. Build a preliminary structure **without assuming behavior**

### Phase 2: Ultra-Granular Function Analysis

For **every** function in scope, document:

1. **Purpose** — Why the function exists
2. **Inputs & Assumptions** — Parameters and implicit inputs
3. **Outputs & Effects** — Return values, state writes, events, external calls
4. **Block-by-Block Analysis** — Apply First Principles, 5 Whys, 5 Hows per block

**External Call Handling**:
- If code exists: treat as internal call, trace fully
- If black box: analyze as adversarial — consider revert, incorrect return, unexpected state changes, reentrancy

**Continuity Rule**: Treat the entire call chain as one continuous execution flow. Never reset context mid-chain.

**Quality Thresholds per Function**:
- Minimum 3 invariants documented
- Minimum 5 assumptions documented
- Minimum 3 risk considerations for external interactions
- At least 1 First Principles application
- At least 3 combined 5 Whys/5 Hows applications

### Phase 3: Global System Understanding

1. **State & Invariant Reconstruction** — What must always hold?
2. **Workflow Reconstruction** — What are the main execution flows?
3. **Trust Boundary Mapping** — Who trusts whom?
4. **Complexity & Fragility Clustering** — Where are the highest-risk areas?

## Anti-Hallucination Rules

- Never reshape evidence to fit earlier assumptions
- Periodically anchor key facts explicitly in writing
- Avoid vague guesses — express uncertainty explicitly
- Cross-reference assumptions with code constantly

## Rationalizations to Reject

| Rationalization | Why It's Wrong |
|-----------------|----------------|
| "I get the gist" | Gist misses edge cases that cause bugs |
| "This function is simple" | Simple functions compose into complex bugs |
| "I'll remember this invariant" | Context degrades; write it down |
| "External call is probably fine" | External = adversarial until proven otherwise |
| "I can skip this helper" | Helpers contain assumptions that propagate |
| "This is taking too long" | Rushed context → hallucinated vulnerabilities |

## Output Format

```markdown
## Code Understanding: [Target]

### Module Map
[Major modules and their purposes]

### Function Analysis: [FunctionName]
**Purpose**: [Why it exists]
**Inputs**: [Parameters + implicit inputs]
**State Changes**: [What it modifies]
**External Calls**: [Who it calls and assumptions]

**Block Analysis**:
- Lines N-M: [What happens and why]
  - Why: [5 Whys application]
  
**Invariants**:
1. [Always-true property]
2. [Always-true property]
3. [Always-true property]

**Assumptions**:
1. [Assumed precondition]
...

### Global Invariants
[System-wide properties that must always hold]

### Trust Boundaries
[Who trusts what and under what conditions]

### High-Risk Areas
[Functions/components with most complexity/external interaction]
```
