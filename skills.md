# Skills Template Standard

All skills must follow this template so they can be discovered, executed, and reported consistently.

## Required Folder Structure

```text
<skill-name>/
├── reference/
│   ├── rules.md
│   └── report-template.md
```

## Required Files

### `reference/rules.md`
- Defines the operational rules for the skill.
- Must include usage constraints, expected inputs, execution steps, and output expectations.
- `skills.md` is the canonical reference for requiring this file.

### `reference/report-template.md`
- Defines the report format produced by the skill.
- When a skill is invoked, its output report should be generated in the structure defined by this template.
- At minimum, include sections for `Summary`, `Findings`, and `Recommendations`.

## Example

```text
sample/
├── reference/
│   ├── rules.md
│   └── report-template.md
```
