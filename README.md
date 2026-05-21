# Secure AI Coding — Skills Library

A categorized library of security-focused skills for [Claude Code](https://claude.ai/code), adapted from the [Trail of Bits skills](https://github.com/trailofbits/skills) repository.

Each skill lives in `skills/<category>/<skill-name>/SKILL.md` and may include reference documents in `skills/<category>/<skill-name>/reference/` or `references/` that are invoked during execution.

---

## Repository Structure

```
skills/
├── _shared/
│   ├── report-template.md      # Universal audit report template
│   └── utils.yaml              # Shared defaults, batches, negative patterns
├── secrets-detector/
│   ├── SKILL.md
│   └── reference/
│       └── rules.yaml          # 6 optimized detection rules
├── injection-scanner/
│   └── SKILL.md
├── static-analysis/
├── security-auditing/
├── smart-contracts/
├── testing/
├── threat-intel/
├── workflow/
├── developer-tools/
├── reverse-engineering/
└── utilities/
```

---

## Analytics

### Skill Inventory

| Metric | Count |
|--------|------:|
| Total skills | **42** |
| Categories | **9** |
| Reference / support files | **97** |
| Secrets-detector detection rules | **6** |

### Skills by Category

| Category | Skills | Description |
|----------|-------:|-------------|
| [static-analysis](#static-analysis) | 6 | Writing and running static analysis rules |
| [security-auditing](#security-auditing) | 7 | Security code review and vulnerability detection |
| [developer-tools](#developer-tools) | 6 | Developer productivity and code quality |
| [workflow](#workflow) | 5 | Meta-skills for improving analysis quality |
| [utilities](#utilities) | 5 | General-purpose and process utilities |
| [threat-intel](#threat-intel) | 4 | Threat detection, malware analysis, CI/CD security |
| [smart-contracts](#smart-contracts) | 4 | Blockchain and smart contract security |
| [testing](#testing) | 2 | Advanced testing methodologies |
| [reverse-engineering](#reverse-engineering) | 1 | Binary analysis and low-level inspection |
| [standalone](#standalone-skills) | 2 | Skills at the skills/ root |
| **Total** | **42** | |

### Tool Usage Across All Skills

| Tool | Skills Using It | Coverage |
|------|----------------:|---------|
| `Read` | 42 | 100% |
| `Bash` | 41 | 98% |
| `Grep` | 35 | 83% |
| `Glob` | 35 | 83% |
| `Write` | 20 | 48% |
| `Edit` | 13 | 31% |
| `WebFetch` | 7 | 17% |
| `AskUserQuestion` | 2 | 5% |
| `WebSearch` | 1 | 2% |

### Secrets Detector — Optimization Impact

The `secrets-detector` skill applies all 10 advanced optimizations from the skill design spec:

| Optimization | Mechanism | Token Saving | Accuracy Gain | Speed Gain |
|---|---|:-:|:-:|:-:|
| Batch evaluation | Rules grouped by `file_types`; only matching batches load | ~70% | — | +300% |
| Per-file caching | Session-TTL cache keyed by `path:mtime` | 50–80% | — | +400% |
| Max file size gate | `max_file_size_kb` skips minified/generated files | 10–40% | — | +500% |
| `file_types` pre-filter | Top-level extension check before any regex | 20–50% | — | +150% |
| Fast-hash pre-screen | Keyword grep before full regex run | ~30% | +10% | +200% |
| Comment exclusion | `exclude_comments` strips `#`, `//`, `--`, etc. | ~5% | +35% | +20% |
| `min_line_length` | Ignores lines < 8 chars | ~10% | +15% | +50% |
| Anchored regex (`\b`) | Word-boundary on all key terms | — | +40% | +10% |
| Confidence scoring | Weighted positive / negative pattern signals | — | +50% | — |
| Context capture | `context_lines` before/after violation | — | +25% | — |

---

## Skill Reference

### Standalone Skills

Skills located directly under `skills/` without a subcategory:

| Skill | Description | Tools | Rules |
|-------|-------------|-------|------:|
| [secrets-detector](./skills/secrets-detector/) | Detects hardcoded secrets, credentials, and high-entropy tokens in source code and configuration files | `Bash` `Read` `Glob` `Grep` `Write` | 6 |
| [injection-scanner](./skills/injection-scanner/) | Scans code for injection vulnerabilities | — | — |

---

### Static Analysis

Tools for writing and running static analysis rules.

| Skill | Description | Tools |
|-------|-------------|-------|
| [semgrep-rule-creator](./skills/static-analysis/semgrep-rule-creator/) | Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns | `Bash` `Read` `Write` `Edit` `Glob` `Grep` `WebFetch` |
| [semgrep-rule-variant-creator](./skills/static-analysis/semgrep-rule-variant-creator/) | Creates language variants of existing Semgrep rules | `Bash` `Read` `Write` `Edit` `Glob` `Grep` `WebFetch` |
| [variant-analysis](./skills/static-analysis/variant-analysis/) | Finds similar vulnerabilities across codebases after identifying an initial pattern | `Bash` `Read` `Glob` `Grep` `WebFetch` |
| [codeql](./skills/static-analysis/codeql/) | CodeQL security vulnerability scanning with interprocedural data flow and taint tracking | `Bash` `Read` `Write` `Glob` `Grep` `WebFetch` |
| [semgrep](./skills/static-analysis/semgrep/) | Executes Semgrep security scans with parallel language detection | `Bash` `Read` `Write` `Glob` `Grep` |
| [sarif-parsing](./skills/static-analysis/sarif-parsing/) | Parses, analyzes, and processes SARIF files from security tools | `Bash` `Read` `Write` `Glob` `Grep` |

---

### Security Auditing

Methodologies for security code review and vulnerability detection.

| Skill | Description | Tools |
|-------|-------------|-------|
| [insecure-defaults](./skills/security-auditing/insecure-defaults/) | Detects fail-open vulnerabilities where applications operate insecurely due to missing configuration | `Bash` `Read` `Glob` `Grep` |
| [sharp-edges](./skills/security-auditing/sharp-edges/) | Identifies security design patterns in APIs and interfaces that enable developer misuse | `Read` `Bash` `Grep` `Glob` |
| [zeroize-audit](./skills/security-auditing/zeroize-audit/) | Detects missing or ineffective zeroization of sensitive data in C/C++ and Rust codebases | `Bash` `Read` `Glob` `Grep` |
| [c-review](./skills/security-auditing/c-review/) | Orchestrates a multi-phase security code review for C/C++ codebases using parallel specialized agents | `Bash` `Read` `Write` `Glob` `Grep` |
| [constant-time-analysis](./skills/security-auditing/constant-time-analysis/) | Detects timing side-channel vulnerabilities in cryptographic implementations across 13 languages | `Bash` `Read` `Glob` `Grep` |
| [differential-review](./skills/security-auditing/differential-review/) | Risk-first security review of PRs, commits, and diffs | `Bash` `Read` `Glob` `Grep` |
| [supply-chain-risk-auditor](./skills/security-auditing/supply-chain-risk-auditor/) | Identifies dependencies at heightened risk of exploitation or takeover | `Bash` `Read` `Write` `Glob` `Grep` |

---

### Smart Contracts

Security tools for blockchain and smart contract codebases.

| Skill | Description | Tools |
|-------|-------------|-------|
| [building-secure-contracts](./skills/smart-contracts/building-secure-contracts/) | Security patterns, best practices, and vulnerability guidance for smart contract development | `Read` `Bash` `Glob` `Grep` `WebFetch` |
| [entry-point-analyzer](./skills/smart-contracts/entry-point-analyzer/) | Maps all state-changing externally callable functions in smart contract codebases | `Bash` `Read` `Glob` `Grep` |
| [spec-to-code-compliance](./skills/smart-contracts/spec-to-code-compliance/) | Verifies blockchain implementations against their specifications | `Read` `Bash` `Glob` `Grep` `WebFetch` |
| [dimensional-analysis](./skills/smart-contracts/dimensional-analysis/) | Annotates codebases with unit and dimension analysis to identify arithmetic bugs in DeFi protocols | `Bash` `Read` `Write` `Edit` `Glob` `Grep` |

---

### Testing

Advanced testing methodologies beyond example-based tests.

| Skill | Description | Tools |
|-------|-------------|-------|
| [property-based-testing](./skills/testing/property-based-testing/) | Guidance for property-based testing across multiple languages and smart contracts | `Bash` `Read` `Write` `Edit` `Glob` `Grep` |
| [mutation-testing](./skills/testing/mutation-testing/) | Mutation testing campaign configuration using mewt/muton | `Bash` `Read` `Write` `Edit` `Glob` `Grep` |

---

### Threat Intel

Tools for threat detection, malware analysis, and CI/CD security.

| Skill | Description | Tools |
|-------|-------------|-------|
| [agentic-actions-auditor](./skills/threat-intel/agentic-actions-auditor/) | Audits GitHub Actions workflows for vulnerabilities in AI agent integrations | `Bash` `Read` `Glob` `Grep` |
| [yara-authoring](./skills/threat-intel/yara-authoring/) | Authors and validates YARA rules for malware detection and threat hunting | `Bash` `Read` `Write` `Edit` `Glob` `Grep` |
| [firebase-apk-scanner](./skills/threat-intel/firebase-apk-scanner/) | Scans Android APKs for Firebase misconfigurations and security vulnerabilities | `Bash` `Read` `Write` `Glob` `Grep` |
| [burpsuite-project-parser](./skills/threat-intel/burpsuite-project-parser/) | Searches and explores Burp Suite project files from the command line | `Bash` `Read` |

---

### Workflow

Meta-skills for improving analysis quality and process.

| Skill | Description | Tools |
|-------|-------------|-------|
| [audit-context-building](./skills/workflow/audit-context-building/) | Systematically builds deep code understanding before beginning a security audit | `Read` `Bash` `Grep` `Glob` |
| [ask-questions-if-underspecified](./skills/workflow/ask-questions-if-underspecified/) | Pauses to ask clarifying questions when task requirements are unclear | `AskUserQuestion` |
| [workflow-skill-design](./skills/workflow/workflow-skill-design/) | Designs new Claude Code skills with proper structure, anti-patterns, and reference documentation | `Read` `Write` `Edit` `Bash` `Glob` `Grep` |
| [second-opinion](./skills/workflow/second-opinion/) | Runs external LLM code reviews (OpenAI Codex or Google Gemini CLI) on uncommitted changes | `Bash` `Read` `Glob` `Grep` `AskUserQuestion` |
| [skill-improver](./skills/workflow/skill-improver/) | Iteratively reviews and fixes Claude Code skill quality issues | `Read` `Write` `Edit` `Bash` `Glob` `Grep` |

---

### Developer Tools

Developer productivity and code quality tools.

| Skill | Description | Tools |
|-------|-------------|-------|
| [devcontainer-setup](./skills/developer-tools/devcontainer-setup/) | Creates isolated development container configurations for Python, Node/TypeScript, Rust, and Go projects | `Bash` `Read` `Write` `Edit` `Glob` `Grep` |
| [fp-check](./skills/developer-tools/fp-check/) | Verifies whether security findings are genuine vulnerabilities or false positives | `Bash` `Read` `Glob` `Grep` |
| [gh-cli](./skills/developer-tools/gh-cli/) | GitHub CLI workflows for common repository operations including PR management and CI status | `Bash` `Read` |
| [git-cleanup](./skills/developer-tools/git-cleanup/) | Safely analyzes and deletes stale local git branches and worktrees | `Bash` `Read` |
| [modern-python](./skills/developer-tools/modern-python/) | Modernizes Python projects to use uv, ruff, and ty | `Bash` `Read` `Write` `Edit` `Glob` `Grep` |
| [seatbelt-sandboxer](./skills/developer-tools/seatbelt-sandboxer/) | Generates minimal allowlist-based macOS Seatbelt sandbox configurations | `Bash` `Read` `Write` `Edit` |

---

### Reverse Engineering

Tools for binary analysis and low-level code inspection.

| Skill | Description | Tools |
|-------|-------------|-------|
| [dwarf-expert](./skills/reverse-engineering/dwarf-expert/) | Provides expertise for analyzing DWARF debug information and understanding the DWARF standard (v3–v5) | `Read` `Bash` `Grep` `Glob` `WebSearch` |

---

### Utilities

General-purpose and process utility skills.

| Skill | Description | Tools |
|-------|-------------|-------|
| [culture-index](./skills/utilities/culture-index/) | Interprets Culture Index psychometric profiles for individuals and teams | `Read` |
| [debug-buttercup](./skills/utilities/debug-buttercup/) | Debugs the Buttercup CRS running on Kubernetes | `Bash` `Read` |
| [trailmark](./skills/utilities/trailmark/) | Parses source code into directed graphs for attack surface mapping and audit prioritization | `Bash` `Read` `Glob` `Grep` |
| [let-fate-decide](./skills/utilities/let-fate-decide/) | Draws 4 Tarot cards using cryptographic randomness to inject entropy into planning | `Bash` `Read` |
| [testing-handbook-skills](./skills/utilities/testing-handbook-skills/) | Security testing skills from the Trail of Bits Testing Handbook (fuzzing, sanitizers, coverage) | `Bash` `Read` `Write` `Edit` `Glob` `Grep` `WebFetch` |

---

## Shared Resources

| File | Purpose |
|------|---------|
| [`skills/_shared/report-template.md`](./skills/_shared/report-template.md) | Universal audit report: executive summary, scan statistics, per-finding evidence blocks with context lines, false-positive notes, recommendations |
| [`skills/_shared/utils.yaml`](./skills/_shared/utils.yaml) | Shared defaults (`max_file_size_kb`, `min_line_length`, `context_lines`, cache TTL), comment token list, reusable negative patterns with confidence weights, named file-type batch definitions |

---

## Adding a New Skill

```
skills/<category>/<skill-name>/
├── SKILL.md                  # Required — frontmatter + execution instructions
└── reference/
    ├── rules.yaml            # Detection rules (use optimized format)
    └── report-template.md   # Optional override of _shared/report-template.md
```

**Minimum `SKILL.md` frontmatter:**

```yaml
---
name: my-skill
description: One sentence. Use when <trigger condition>.
allowed-tools: Bash Read Glob Grep
---
```

**Minimum `rules.yaml` entry** (optimized format):

```yaml
rules:
  - id: MY-001
    name: "Rule Name"
    severity: high           # critical | high | medium | low
    file_types: [".py", ".js"]
    max_file_size_kb: 100
    min_line_length: 8
    exclude_comments: true
    detection:
      type: hybrid
      regex_pattern: '\bpattern\b'
      fallback_command: 'grep -En "pattern" {{file}}'
      fallback_min_size_kb: 500
      context_lines: 1
    confidence:
      positive_patterns:
        - pattern: '...'
          weight: 0.5
      negative_patterns:
        - pattern: '...'
          weight: -0.5
      threshold: 0.7
    remediation: "What to do."
    references: ["CWE-XXX", "OWASP AXX:YYYY"]
```

---

*Skills adapted from the [Trail of Bits skills](https://github.com/trailofbits/skills) repository.*
