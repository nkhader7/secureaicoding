---
name: injection-scanner
description: Detect command/SQL/template injection patterns using batched, cache-aware, confidence-scored rule evaluation.
allowed-tools: Bash Read
---

# Injection Scanner

Use `reference/rules.yaml` and shared report format from `../_shared/report-template.md`.

## Execution Workflow
1. Load rules, then select only matching `batches` for discovered file extensions.
2. Cache per-file results by `$file_path:$file_mtime` to avoid duplicate scans across multiple rules.
3. Apply rule pre-filters before regex execution:
   - `file_types`
   - `max_file_size_kb`
   - `min_line_length`
   - `exclude_comments`
4. Evaluate detection and confidence:
   - anchored regex for variable boundaries
   - weighted confidence signals
   - threshold gating to suppress weak hits
5. Include `context_lines` evidence and actionable remediation text.
