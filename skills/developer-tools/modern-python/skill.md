---
name: modern-python
description: Modernizes Python projects to use uv (package management), ruff (linting/formatting), and ty (type checking). Use when setting up a new Python project, migrating from pip/Poetry/mypy/black, or updating Python tooling.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Modern Python

Configures Python projects with modern tools: **uv** (package management), **ruff** (linting/formatting), and **ty** (type checking).

## When to Use

- Setting up new Python projects
- Migrating from pip/Poetry/mypy/black to modern tooling
- Configuring standalone scripts with dependencies
- Modernizing existing Python projects

## When NOT to Use

- User explicitly wants legacy tooling
- Requires Python <3.11
- Non-Python codebases

## Tool Replacements

| Legacy | Modern |
|--------|--------|
| pip + requirements.txt | **uv** |
| flake8 + black + isort | **ruff** |
| mypy/pyright | **ty** |
| pre-commit | **prek** |
| Poetry | **uv** |

## Core Principles

- Always use `uv add`/`uv remove` for dependency management
- Never manually activate virtual environments — use `uv run`
- Use `[dependency-groups]` per PEP 735 instead of optional dependencies
- Target Python 3.11+ exclusively

## Three Setup Paths

### 1. Quick Start (Simple Projects)

```bash
uv init myproject
cd myproject
uv add ruff --group dev
```

### 2. Full Setup (Distributable Packages)

Use the Trail of Bits cookiecutter template for production-ready configuration with all tools preconfigured.

### 3. Migration (Existing Codebases)

See [migration-checklist.md](references/migration-checklist.md) for systematic conversion.

## Key Configuration (`pyproject.toml`)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = ["ruff>=0.8", "ty>=0.1"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "S", "B", "A"]
ignore = []

[tool.ty]
strict = true
error-on-warning = true
```

## Essential Commands

```bash
# Package management
uv add <package>           # Add dependency
uv add --group dev <pkg>  # Add dev dependency
uv remove <package>        # Remove dependency
uv sync                    # Install all dependencies
uv run python script.py    # Run without activating venv

# Code quality
uv run ruff check .        # Lint
uv run ruff format .       # Format
uv run ty check .          # Type check

# Testing
uv run pytest
```

## Reference Files

- [migration-checklist.md](references/migration-checklist.md) — Step-by-step legacy → modern migration
- [pyproject.md](references/pyproject.md) — Complete pyproject.toml reference
- [uv-commands.md](references/uv-commands.md) — uv CLI reference
- [ruff-config.md](references/ruff-config.md) — Ruff rule configuration
- [pep723-scripts.md](references/pep723-scripts.md) — Standalone scripts with inline dependencies
