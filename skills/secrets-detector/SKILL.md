---
name: secrets-detector
description: Detect hardcoded secrets with high-signal heuristics, confidence scoring, and performance-aware scanning.
allowed-tools: Bash Read
---

# Secrets Detector

Use `reference/rules.yaml` as the authoritative configuration. Optimize for fast pre-filtering and low false positives.

## Execution Workflow
1. Load rules and group by `batches[*].file_types`.
2. Discover target files and map by extension.
3. For each file, apply pre-filters in order:
   - extension in rule `file_types`
   - file size <= `max_file_size_kb` (unless hybrid fallback applies)
4. Build cache key `${file_path}:${file_mtime}` and reuse prior results if present.
5. For each line:
   - skip if line length < `min_line_length`
   - if `exclude_comments` is true, skip lines where first non-space token is `#`, `//`, or `--`
6. Evaluate rule detection:
   - use `detection.type: regex` or `hybrid`
   - for `hybrid`, run `fallback_command` only when file size > `fallback_min_size_kb` and Bash is available
7. Compute confidence score from weighted patterns; report only when score >= `confidence.threshold`.
8. Include evidence with `context_lines` before/after violation line.
9. Emit findings into `../_shared/report-template.md` structure.

## Accuracy Controls
- Prefer anchored boundaries (`\\b`) in regex.
- Use negative confidence weights for safe usage patterns (e.g., `env(...)`).
- Preserve line numbers and context to improve remediation quality.
