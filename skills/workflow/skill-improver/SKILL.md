---
name: skill-improver
description: Iteratively reviews and fixes Claude Code skill quality issues. Use for sustained skill refinement with multiple issues or when onboarding a new skill.
allowed-tools: Read Write Edit Bash Glob Grep
---

# Skill Improver

Iteratively reviews and fixes Claude Code skill quality issues using structured feedback.

## When to Use

- Sustained refinement effort for skills with multiple issues
- Quality review of a newly created skill before deployment
- Fixing skills that fail to trigger or have weak descriptions

## When NOT to Use

- Single one-time review (use the skill-reviewer agent directly)
- Reviewing external/third-party skills

## Issue Severity Hierarchy

### Critical (Fix Immediately)
- Missing required frontmatter fields (`name`, `description`)
- Invalid YAML syntax in frontmatter
- These block skill loading or cause runtime failures

### Major (Fix Next)
- Weak trigger descriptions that fail to invoke the skill
- Vague or inaccurate `description` field (controls when Claude uses the skill)
- Missing `allowed-tools` specification

### Minor (Evaluate Individually)
- Polish items: clarity, examples, formatting
- Only implement if clearly beneficial
- Don't implement minor fixes that could introduce regressions

## Iteration Framework

```
Loop:
1. Review — Run skill-reviewer, identify all issues
2. Categorize — Classify as Critical, Major, or Minor
3. Fix — Address Critical and Major issues
4. Evaluate — Assess each Minor issue individually
5. Repeat until all Critical/Major fixed and Minors evaluated
```

## Frontmatter Requirements

```yaml
---
name: skill-name         # required: lowercase, hyphenated
description: >           # required: triggers when Claude uses this skill
  Specific trigger condition. Use when X. Triggers on Y pattern.
allowed-tools: Read Bash Glob Grep  # recommended: list permitted tools
---
```

## Writing Effective Descriptions

The `description` field controls **when Claude invokes the skill**. It must be:

- **Specific**: Vague descriptions cause under-triggering or over-triggering
- **Trigger-oriented**: Include "Use when...", "Triggers on...", "Activates when..."
- **Keyword-rich**: Include key terms users will say

**Weak**: "Helps with code analysis"

**Strong**: "Detects timing side-channel vulnerabilities in cryptographic code. Use when auditing code that processes secrets, keys, tokens, or authentication data."

## Completion Marker

When all Critical and Major issues are fixed and Minors have been evaluated:

```
<skill-improvement-complete>
All critical and major issues resolved.
Remaining minor items evaluated — [N accepted, M deferred].
</skill-improvement-complete>
```

The stop condition checks **only** for this marker.
