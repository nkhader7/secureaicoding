---
name: agentic-actions-auditor
description: Audits GitHub Actions workflows for vulnerabilities in AI agent integrations. Use when reviewing CI/CD pipelines that use Claude Code Action, Gemini CLI, OpenAI Codex, or GitHub AI Inference.
allowed-tools: Bash Read Glob Grep
---

# Agentic Actions Auditor

Audits GitHub Actions workflows for attack vectors where attacker-controlled input reaches AI agents in CI/CD pipelines.

## When to Use

- Reviewing `.github/workflows/` for AI agent integrations
- Security assessment of CI/CD pipelines using Claude Code Action, Gemini CLI, OpenAI Codex, or GitHub AI Inference
- Pre-deployment review of agentic workflow configurations

## Supported AI Actions

The auditor identifies these AI agent steps by `uses:` prefix:
- `anthropics/claude-code-action`
- `google/gemini-cli-action`
- `openai/codex-action`
- `github/ai-inference`

## Five-Step Audit Process

1. **Discover** workflow files in `.github/workflows/`
2. **Identify** AI action steps by matching `uses:` prefixes
3. **Capture** security context (triggers, env vars, permissions, prompt fields)
4. **Analyze** nine attack vectors (A–I)
5. **Report** findings with severity, evidence, data flow traces, and remediation

## Nine Attack Vectors

| Vector | Description |
|--------|-------------|
| A | Direct prompt injection via issue/PR body |
| B | Environment variable intermediary to prompt |
| C | Workflow file contents used as prompt input |
| D | External data fetched into prompt context |
| E | Tool output fed back into agent prompts |
| F | Sandbox escape via tool configuration |
| G | Secret exfiltration via AI agent outputs |
| H | Indirect injection through repository content |
| I | Trigger-based privilege escalation |

## Critical Findings to Flag

**Dangerous trigger combinations**:
```yaml
on:
  pull_request_target:    # Runs in privileged context with PR body access
    types: [opened, synchronize]
```

**Environment variable to prompt flow** (often missed in manual review):
```yaml
- uses: anthropics/claude-code-action@v1
  env:
    ISSUE_BODY: ${{ github.event.issue.body }}  # Attacker-controlled
  with:
    prompt: "Process this request"
    # ISSUE_BODY flows into agent context even without explicit prompt reference
```

**Permissive sandbox configuration**:
```yaml
with:
  allowed-tools: "Bash"  # Unrestricted bash = full code execution
  sandbox: false          # No sandbox at all
```

## Important Constraints to Reject

- **"Restricted tools guarantee safety"** → Tool restrictions don't prevent prompt injection; agents can still be manipulated to misuse allowed tools
- **"Sandbox is enabled, so we're safe"** → Sandboxes require proper configuration; misconfigured sandboxes provide false security
- **"Only maintainers can trigger this"** → `pull_request_target` exposes workflows to PR authors regardless of maintainer policies
- **"The prompt doesn't contain variables"** → Data can flow through `env:` blocks without appearing in the prompt field

## Remediation Patterns

```yaml
# Require explicit approval before AI agent runs
- name: Check PR author permission
  uses: actions/github-script@v7
  with:
    script: |
      const { data: perm } = await github.rest.repos.getCollaboratorPermissionLevel({
        owner: context.repo.owner, repo: context.repo.repo,
        username: context.payload.pull_request.user.login
      });
      if (!['admin', 'write'].includes(perm.permission)) {
        core.setFailed('Insufficient permissions');
      }
```
