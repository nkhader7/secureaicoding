---
name: gh-cli
description: GitHub CLI workflows for common repository operations including PR management, issue tracking, and CI status. Use when working with GitHub repositories via the command line.
allowed-tools: Bash Read
---

# GitHub CLI (gh)

Common GitHub CLI workflows for repository operations.

## When to Use

- Creating and reviewing pull requests
- Managing issues
- Checking CI/CD status
- Repository administration tasks
- Scripting GitHub operations

## Prerequisites

```bash
gh auth login  # Authenticate with GitHub
gh auth status # Verify authentication
```

## Common Operations

### Pull Requests

```bash
# Create a PR
gh pr create --title "Title" --body "Description"

# List PRs
gh pr list

# View a PR
gh pr view 123

# Review a PR
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Comments"

# Check PR status
gh pr checks 123

# Merge a PR
gh pr merge 123 --squash --auto
```

### Issues

```bash
# Create an issue
gh issue create --title "Bug report" --body "Description"

# List issues
gh issue list --assignee @me

# View an issue
gh issue view 456

# Close an issue
gh issue close 456
```

### Repository

```bash
# Clone a repo
gh repo clone owner/repo

# Fork a repo
gh repo fork owner/repo

# View repo info
gh repo view

# List releases
gh release list

# Create a release
gh release create v1.0.0 --notes "Release notes"
```

### CI/CD

```bash
# List workflow runs
gh run list

# View a run
gh run view

# Re-run failed jobs
gh run rerun --failed

# Watch a running workflow
gh run watch
```

### API Access

```bash
# Make authenticated API calls
gh api repos/owner/repo/issues

# POST with data
gh api repos/owner/repo/issues --method POST \
  --field title="Title" --field body="Body"
```

## Useful Flags

| Flag | Purpose |
|------|---------|
| `--json` | Output as JSON |
| `--jq` | Filter JSON output |
| `--web` | Open in browser |
| `--assignee @me` | Filter to current user |
| `--limit N` | Limit results |
