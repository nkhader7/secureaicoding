---
name: second-opinion
description: Runs external LLM code reviews (OpenAI Codex or Google Gemini CLI) on uncommitted changes, branch diffs, or specific commits. Use when asking for a second opinion, external review, or mentioning /second-opinion.
allowed-tools: Bash Read Glob Grep AskUserQuestion
---

# Second Opinion

Gets an independent code review from a different AI model (OpenAI Codex CLI or Google Gemini CLI).

## When to Use

- Getting a second opinion from a different model before opening a PR
- Reviewing branch diffs with an independent perspective
- Checking uncommitted work for issues before committing
- Running focused reviews (security, performance, error handling)
- Comparing review output from multiple models

## When NOT to Use

- Neither Codex CLI nor Gemini CLI is installed
- No API key/subscription configured
- Reviewing non-code files (docs, config)

## Safety Note

Gemini CLI is invoked with `--yolo`, which auto-approves all tool calls. Required for headless (non-interactive) operation.

## Invocation

Use `AskUserQuestion` to collect:
1. **Tool**: Both Codex and Gemini (Recommended) / Codex only / Gemini only
2. **Scope**: Uncommitted changes / Branch diff vs main / Specific commit
3. **Context**: Include CLAUDE.md or AGENTS.md if exists?
4. **Focus**: General / Security & auth / Performance / Error handling

## Commands

```bash
# Codex
codex exec --sandbox read-only --ephemeral \
  --output-schema references/codex-review-schema.json \
  -o "$output_file" - < "$prompt_file"

# Gemini
gemini -p "/code-review" --yolo -e code-review
git diff HEAD > /tmp/review-diff.txt
{ printf '%s\n\n' 'Review this diff for issues.'; cat /tmp/review-diff.txt; } \
  | gemini -p - --yolo -m gemini-3.1-pro-preview
```

## Models

- **Codex**: `gpt-5.3-codex`, reasoning: `xhigh`; fallback: `gpt-5.2-codex`
- **Gemini**: `gemini-3.1-pro-preview`, flags: `--yolo`, `-e`, `-m`

## Auto-Detect Default Branch

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null \
  | sed 's@^refs/remotes/origin/@@' || echo main
```

## Running Both

Run Codex and Gemini in **parallel**. Present with clear headers. Summarize where reviews agree and differ.

## Error Handling

| Error | Action |
|-------|--------|
| `codex: command not found` | `npm i -g @openai/codex` |
| `gemini: command not found` | `npm i -g @google/gemini-cli` |
| Model auth error (Codex) | Retry with `gpt-5.2-codex` |
| Empty diff | Tell user there are no changes to review |
| Timeout | Inform user and suggest narrowing scope |

## Reference Files

- [codex-invocation.md](references/codex-invocation.md) — Detailed Codex CLI usage
- [gemini-invocation.md](references/gemini-invocation.md) — Detailed Gemini CLI usage
