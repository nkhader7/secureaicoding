---
name: asvs-v5-skills
description: Use when mapping application security requirements, test cases, or review findings to OWASP ASVS v5.0.0 verification requirements.
---

# OWASP ASVS v5 Skills

Use this skill to convert security requirements and testing activities into ASVS v5-aligned verification tasks and track coverage by ASVS chapter.

## When to Use

- You need to structure a secure coding or testing plan around OWASP ASVS v5.
- You need to map existing findings to ASVS verification requirements.
- You need a repeatable checklist format for security gates in CI/CD.

## When NOT to Use

- You only need a lightweight best-practices list without framework traceability.
- You are auditing domains better covered by a specialized standard (e.g., PCI DSS-only, SOC 2 control mapping-only).

## Rationalizations to Reject

- **"We can skip mapping and just do a scan."** → Scanners miss design/process requirements → map findings and manual checks to ASVS chapters.
- **"ASVS is too broad, we'll pick random controls."** → Random sampling creates blind spots → use chapter-based coverage planning.

## Workflow

1. Determine ASVS level target (L1/L2/L3) for the application risk profile.
2. Select relevant ASVS chapters from `reference/asvs-v5-domains.md`.
3. Build a requirement-to-test matrix with IDs, owners, and evidence links.
4. Execute automated and manual checks.
5. Record pass/fail/waiver status and residual risk.

## Reference Index

- `reference/asvs-v5-domains.md` — ASVS v5 chapter-oriented skill modules.
- `reference/mapping-template.md` — Reusable matrix template for requirement mapping and evidence tracking.
