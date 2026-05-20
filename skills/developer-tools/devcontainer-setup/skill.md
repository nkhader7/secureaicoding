---
name: devcontainer-setup
description: Creates isolated development container configurations for Python, Node/TypeScript, Rust, and Go projects. Use when setting up a devcontainer, creating a reproducible dev environment, or onboarding to a new project.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Dev Container Setup

Creates isolated development environments by generating configuration files in `.devcontainer/`.

## When to Use

- Setting up a reproducible development environment
- Onboarding a new project with a consistent dev container
- Creating a GitHub Codespaces configuration
- Standardizing developer environments across a team

## Language Detection

| Language | Detection Markers |
|----------|------------------|
| Python | `pyproject.toml`, `requirements.txt`, `*.py` files |
| Node/TypeScript | `package.json`, `tsconfig.json` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |

For multi-language projects, priority order: **Python → Node/TypeScript → Rust → Go**

## Generated Files

```
.devcontainer/
├── Dockerfile              # Base image and tool installation
├── devcontainer.json       # Container configuration
├── post-install.sh         # Post-creation setup script
└── shell.sh                # Shell configuration (aliases, env)
```

## Language-Specific Configuration

### Python
- Base: Python 3.13 via uv
- Extensions: Pylance, Ruff
- Post-install: `uv sync`

### Node/TypeScript
- Base: Node 22 via fnm (Fast Node Manager)
- Auto-detects package manager from lockfiles (pnpm, yarn, npm)
- Extensions: ESLint, Prettier

### Rust
- Base: rust-analyzer + cargo
- Supports locked builds when `Cargo.lock` exists
- Extensions: rust-analyzer

### Go
- Base: golang.go extension
- Post-install: `go mod download`

## Base Infrastructure

All devcontainers include:
- Claude Code marketplace plugins
- Modern CLI tools (ripgrep, fzf, jq)
- Token forwarding: `CLAUDE_CODE_OAUTH_TOKEN`, `ANTHROPIC_API_KEY`
- Sandboxing via bubblewrap

## Reference Files

- [dockerfile-best-practices.md](references/dockerfile-best-practices.md) — Dockerfile patterns
- [features-vs-dockerfile.md](references/features-vs-dockerfile.md) — When to use devcontainer features vs. Dockerfile

## Validation Checklist

Before finalizing:
- [ ] All placeholder values substituted with actual project values
- [ ] JSON syntax valid in `devcontainer.json`
- [ ] All detected language extensions included
- [ ] Post-install script is executable (`chmod +x .devcontainer/post-install.sh`)
- [ ] Test by rebuilding container
