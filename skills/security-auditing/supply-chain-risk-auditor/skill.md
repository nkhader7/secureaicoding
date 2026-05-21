---
name: supply-chain-risk-auditor
description: Identifies dependencies at heightened risk of exploitation or takeover. Use when assessing supply chain attack surface, evaluating dependency health, or scoping security engagements.
allowed-tools: Bash Read Write Glob Grep
---

# Supply Chain Risk Auditor

Systematically evaluates project dependencies against specific risk criteria to identify high-risk packages vulnerable to compromise.

## When to Use

- Pre-engagement scoping for security assessments
- Evaluating supply chain attack surface
- Reviewing new dependency additions
- Post-incident investigation of potentially compromised packages

## Prerequisites

- `gh` CLI tool available and authenticated
- Access to target repository

## Risk Factors Evaluated

| Factor | Description |
|--------|-------------|
| Single maintainer | Individual with no organizational backing |
| Unmaintained | Stale repository or explicitly deprecated |
| Low popularity | Few stars/downloads relative to ecosystem |
| High-risk features | FFI, deserialization, code execution capabilities |
| Past CVEs | History of high/critical severity vulnerabilities |
| Missing security contact | No disclosed vulnerability reporting mechanism |

A dependency with **2+ risk factors** is flagged as high-risk.

## Workflow

**Phase 1: Setup**
- Create workspace directory
- Initialize report from [results-template.md](references/results-template.md)
- Identify all dependency files (package.json, requirements.txt, Cargo.toml, go.mod, etc.)

**Phase 2: Audit**
- For each dependency, use `gh` tool queries to obtain accurate metrics
- Never speculate — use exact data from queries
- Document: star count, last commit date, maintainer count, issue count

**Phase 3: Report**
- Document findings in structured tables
- Suggest alternatives for flagged packages
- Summarize risk posture and recommendations

## Key Requirements

- Use exact data from `gh` queries (no speculation or estimation)
- Report only HIGH-risk dependencies (2+ risk factors)
- Provide alternative package suggestions for flagged items
- Include executive summary

## Output Structure

See [results-template.md](references/results-template.md) for the standard report format.
