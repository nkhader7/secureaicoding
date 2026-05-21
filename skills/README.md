# Skills

A categorized library of security-focused skills for Claude Code, adapted from the [Trail of Bits skills](https://github.com/trailofbits/skills) repository.

Each skill lives in `<category>/<skill-name>/skill.md` and may include reference documents in `<category>/<skill-name>/references/` that are invoked by the skill during execution.

## Categories

### [static-analysis/](./static-analysis/)
Tools for writing and running static analysis rules.

| Skill | Description |
|-------|-------------|
| [semgrep-rule-creator](./static-analysis/semgrep-rule-creator/) | Creates custom Semgrep rules for detecting security vulnerabilities |
| [semgrep-rule-variant-creator](./static-analysis/semgrep-rule-variant-creator/) | Creates variants of existing Semgrep rules for broader coverage |
| [variant-analysis](./static-analysis/variant-analysis/) | Finds similar vulnerabilities after identifying an initial pattern |
| [codeql](./static-analysis/codeql/) | CodeQL security scanning with interprocedural data flow analysis |
| [semgrep](./static-analysis/semgrep/) | Executes Semgrep security scans with parallel language detection |
| [sarif-parsing](./static-analysis/sarif-parsing/) | Parses and triages SARIF output from static analysis tools |

### [security-auditing/](./security-auditing/)
Methodologies for security code review and vulnerability detection.

| Skill | Description |
|-------|-------------|
| [insecure-defaults](./security-auditing/insecure-defaults/) | Detects fail-open vulnerabilities from missing secure configuration |
| [sharp-edges](./security-auditing/sharp-edges/) | Identifies API design patterns that enable developer misuse |
| [zeroize-audit](./security-auditing/zeroize-audit/) | Detects missing or ineffective zeroization of sensitive data |
| [c-review](./security-auditing/c-review/) | Multi-phase security code review for C/C++ codebases |
| [constant-time-analysis](./security-auditing/constant-time-analysis/) | Detects timing side-channel vulnerabilities in cryptographic code |
| [differential-review](./security-auditing/differential-review/) | Risk-first security review of PRs, commits, and diffs |
| [supply-chain-risk-auditor](./security-auditing/supply-chain-risk-auditor/) | Identifies dependencies at risk of exploitation or takeover |

### [smart-contracts/](./smart-contracts/)
Security tools for blockchain and smart contract codebases.

| Skill | Description |
|-------|-------------|
| [building-secure-contracts](./smart-contracts/building-secure-contracts/) | Security patterns and best practices for smart contract development |
| [entry-point-analyzer](./smart-contracts/entry-point-analyzer/) | Maps state-changing externally callable functions across contract platforms |
| [spec-to-code-compliance](./smart-contracts/spec-to-code-compliance/) | Verifies blockchain implementations against their specifications |
| [dimensional-analysis](./smart-contracts/dimensional-analysis/) | Analyzes unit and dimensional consistency in smart contract arithmetic |

### [testing/](./testing/)
Advanced testing methodologies beyond example-based tests.

| Skill | Description |
|-------|-------------|
| [property-based-testing](./testing/property-based-testing/) | Property-based testing guidance across multiple languages and smart contracts |
| [mutation-testing](./testing/mutation-testing/) | Mutation testing campaign configuration using mewt/muton |

### [threat-intel/](./threat-intel/)
Tools for threat detection, malware analysis, and CI/CD security.

| Skill | Description |
|-------|-------------|
| [agentic-actions-auditor](./threat-intel/agentic-actions-auditor/) | Audits GitHub Actions workflows for AI agent injection vulnerabilities |
| [yara-authoring](./threat-intel/yara-authoring/) | Authors and validates YARA rules for malware detection |
| [firebase-apk-scanner](./threat-intel/firebase-apk-scanner/) | Scans Android APKs for Firebase misconfigurations and secrets |
| [burpsuite-project-parser](./threat-intel/burpsuite-project-parser/) | Parses Burp Suite project files for security findings |

### [workflow/](./workflow/)
Meta-skills for improving analysis quality and process.

| Skill | Description |
|-------|-------------|
| [audit-context-building](./workflow/audit-context-building/) | Systematically builds context before beginning a security audit |
| [ask-questions-if-underspecified](./workflow/ask-questions-if-underspecified/) | Asks clarifying questions when task requirements are unclear |
| [workflow-skill-design](./workflow/workflow-skill-design/) | Designs new skills with proper structure and anti-patterns |
| [second-opinion](./workflow/second-opinion/) | Gets an independent second opinion on security findings |
| [skill-improver](./workflow/skill-improver/) | Iteratively improves skill quality through structured feedback |

### [developer-tools/](./developer-tools/)
Developer productivity and code quality tools.

| Skill | Description |
|-------|-------------|
| [gh-cli](./developer-tools/gh-cli/) | GitHub CLI workflows for common repository operations |
| [git-cleanup](./developer-tools/git-cleanup/) | Cleans up stale branches and git history |
| [devcontainer-setup](./developer-tools/devcontainer-setup/) | Sets up development container configurations |
| [seatbelt-sandboxer](./developer-tools/seatbelt-sandboxer/) | Creates macOS seatbelt sandbox profiles for process isolation |
| [modern-python](./developer-tools/modern-python/) | Modernizes Python code to use current idioms and tooling |
| [fp-check](./developer-tools/fp-check/) | Analyzes false positive rates in security tool findings |

### [reverse-engineering/](./reverse-engineering/)
Tools for binary analysis and low-level code inspection.

| Skill | Description |
|-------|-------------|
| [dwarf-expert](./reverse-engineering/dwarf-expert/) | Analyzes DWARF debug information in compiled binaries |

### [utilities/](./utilities/)
General-purpose and process utility skills.

| Skill | Description |
|-------|-------------|
| [culture-index](./utilities/culture-index/) | Tracks and documents team culture and engineering norms |
| [debug-buttercup](./utilities/debug-buttercup/) | Structured debugging methodology for complex issues |
| [trailmark](./utilities/trailmark/) | Generates Trail of Bits style security report markup |
| [let-fate-decide](./utilities/let-fate-decide/) | Makes random decisions when options are equivalent |
| [testing-handbook-skills](./utilities/testing-handbook-skills/) | Skills derived from the Trail of Bits Testing Handbook |
