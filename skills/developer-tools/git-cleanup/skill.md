---
name: git-cleanup
description: Safely analyzes and deletes stale local git branches and worktrees. Use when cleaning up merged branches, removing stale feature branches, or tidying a cluttered local git state.
allowed-tools: Bash Read
---

# Git Cleanup

Safely analyzes and deletes local git branches and worktrees through a two-gate confirmation process.

## When to Use

- Cleaning up merged branches after a sprint
- Removing stale feature branches that were abandoned
- Tidying a cluttered local git repository
- Cleaning up worktrees from finished experiments

## When NOT to Use

- Cleaning remote branches (this is local only)
- Force-deleting branches with unmerged work without explicit confirmation

## Safety Principles

- Always use `-d` (safe delete) for merged branches, never `-D` without explicit confirmation
- Detect dirty worktrees before cleanup
- Never touch protected branches (main, master, develop, release/*)
- Two-gate confirmation: show plan → confirm → execute

## Workflow

### Phase 1: Analysis (No Deletions)

```bash
# List all local branches with status
git branch -vv

# Find merged branches
git branch --merged main

# Find branches with no remote tracking
git branch -vv | grep ': gone]'

# List worktrees
git worktree list
```

### Phase 2: Categorization

Group branches by category:
- **Merged**: Fully merged into default branch
- **Squash-merged**: Merged via squash (not shown by `--merged`)
- **Superseded**: Replaced by a newer branch
- **Stale**: No commits for >30 days, no remote tracking

### Phase 3: Confirmation Gate 1

Present the deletion plan:
```
Proposed deletions:
  Merged:     feature/auth-v2, fix/login-bug, chore/deps
  Stale:      feature/old-experiment (no activity for 45 days)

Protected (keeping): main, develop

Proceed? [y/N]
```

### Phase 4: Execute

```bash
# Safe delete (only if merged)
git branch -d feature/auth-v2

# Force delete (require explicit confirmation per branch)
git branch -D stale-branch  # Only after user confirms

# Remove gone worktrees
git worktree prune
```

### Phase 5: Confirmation Gate 2

Report what was deleted and what was kept.

## Detecting Squash-Merges

```bash
# Check if branch has been squash-merged into main
git log main --oneline | grep "$(git log --oneline <branch> | head -1 | awk '{print $2}')"
```

Or use the ancestor check:
```bash
git merge-base --is-ancestor <branch> main
```
