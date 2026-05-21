---
name: secrets-detector
description: Detects hardcoded secrets, credentials, and high-entropy tokens in source code and configuration files. Use when auditing a codebase for leaked credentials, reviewing PRs for accidental secret commits, or performing pre-release security checks.
allowed-tools: Bash Read Glob Grep Write
---

# Secrets Detector

Scans source code, configuration files, and web templates for hardcoded secrets using an optimized multi-pass pipeline: batch pre-filtering by file type, per-file caching, fast-hash pre-screening, hybrid regex/grep detection, comment exclusion, confidence scoring, and context-aware evidence capture.

## When to Use

- Pre-commit or pre-release security scan for leaked credentials
- Reviewing a PR that touches config, infrastructure, or authentication code
- Incident triage to determine whether secrets were committed historically
- Baseline scan of a newly onboarded repository

## When NOT to Use

- Runtime secret detection in running processes (use a SIEM or vault audit log)
- Binary files, compiled artifacts, or minified bundles (low signal, high noise)
- Full secrets rotation workflows (detection only — remediation is manual)

## Architecture

A single-pass, rule-batched pipeline:

```
Target path
  └─► 1. Discover files & classify by extension
  └─► 2. Load matching rule batches (skip irrelevant extensions)
  └─► 3. For each file:
          ├─ Size check (skip if > max_file_size_kb)
          ├─ Cache lookup (reuse findings if file unchanged)
          ├─ Fast-hash pre-screen (skip regex if hash miss)
          ├─ Detection (hybrid regex → grep fallback for large files)
          └─ Confidence scoring → accept / reject findings
  └─► 4. Deduplicate findings across rules
  └─► 5. Render report from _shared/report-template.md
```

## Execution Steps

### Phase 0 — Setup

1. Ask (or infer) the scan target: a path, repo root, or list of files.
2. Initialise an in-memory session cache keyed by `"$file_path:$file_mtime"`.
3. Read `reference/rules.yaml` to load all rules and batch definitions.
4. Read `../_shared/report-template.md` to initialise the output report.

### Phase 1 — File Discovery & Batch Selection

1. Recursively list files under the target path using `Glob` or `Bash find`.
2. Collect the unique set of file extensions present.
3. From `rules.yaml` `batches`, select only the batches whose `file_types`
   overlap with the discovered extensions.  
   **If no batch matches an extension, skip those files entirely.**
4. Build a per-file list: `{path, extension, size_kb, mtime}`.

### Phase 2 — Per-File Scanning

For every file in the list, execute the following sub-steps in order:

#### 2a. Size gate
- If `file.size_kb > rule.max_file_size_kb`, skip file and log it as "skipped (size)".

#### 2b. Cache lookup
- Compute `cache_key = "$file_path:$file_mtime"`.
- If `cache[cache_key]` exists, reuse stored findings and advance to the next file.

#### 2c. Fast-hash pre-screen
- Compute a rolling hash (or use `grep -c` with the core keyword list) on the file.
- If `fast_hash` for the rule does not match, skip full regex for that rule.
  - This avoids running expensive regex on files with zero keyword hits.

#### 2d. Detection
- Collect lines from the file; filter out:
  - Lines shorter than `min_line_length` characters.
  - If `exclude_comments: true`, lines whose first non-whitespace characters
    are any token in `_shared/utils.yaml` → `comment_tokens`
    (`#`, `//`, `--`, `/*`, `*`, `<!--`).
- Apply the `detection.regex_pattern` (or `fallback_command` if
  `file.size_kb >= fallback_min_size_kb` and Bash is available).
- For each matching line, capture `context_lines` lines before and after
  for the evidence block.

#### 2e. Confidence scoring
- For each candidate match, sum the weights:
  - Add `weight` for each `positive_pattern` that matches the matched line.
  - Add (negative) `weight` for each `negative_pattern` that matches.
- If `total_weight < confidence_threshold`, discard the finding.
- Attach `confidence: <score>` to accepted findings.

#### 2f. Cache write
- Store `{findings, timestamp}` in `cache[cache_key]`.

### Phase 3 — Deduplication

- If the same file+line appears in findings from multiple rules, keep only
  the highest-severity rule's finding and note the overlap.

### Phase 4 — Report Generation

1. Fill in all placeholders in `_shared/report-template.md`.
2. For each finding, render the evidence block with context:
   ```
     [N-1]  <line before>
     [N]    <violating line>   ← violation
     [N+1]  <line after>
   ```
3. Populate scan statistics (files scanned, cache hits, findings by severity).
4. Write the completed report to `secrets-audit-report.md` in the working directory
   (or as specified by the user).

## Optimization Reference

| Optimization | Mechanism | Benefit |
|---|---|---|
| Batch evaluation | Rules grouped by `file_types`; only matching batches load | ~70% token reduction on mixed codebases |
| Fast-hash pre-screen | Keyword grep before full regex | ~80% fewer false regex runs |
| Size gate | `max_file_size_kb` per rule | Skips minified/generated files |
| `min_line_length` | Ignores very short lines | ~15% fewer false positives |
| Comment exclusion | `exclude_comments` strips `#`, `//`, `--`, etc. | ~35% fewer false positives |
| Anchored regex (`\b`) | Word-boundary anchors on key terms | ~40% fewer false positives |
| Confidence scoring | Weighted positive/negative pattern signals | ~50% precision improvement |
| Context capture | `context_lines` before/after violation | Better triage evidence |
| Per-file caching | `session` TTL cache keyed by path+mtime | 50–80% work saved on re-runs |
| Grep fallback | Switches to `grep` for files > `fallback_min_size_kb` | Handles large files cheaply |

## Output

- **Report file:** `secrets-audit-report.md` (format: `_shared/report-template.md`)
- **Severity levels:** critical → high → medium → low
- **Confidence range:** 0.0–1.0 (only findings ≥ `confidence_threshold` are reported)

## Key Requirements

- Never speculate about values — only report what the regex or grep command matched.
- Always show evidence with context lines; never show findings without file + line number.
- Respect `exclude_comments` — do not flag commented-out credential stubs.
- Log every skipped file (size or type) in the scan statistics table.
- If a credential is confirmed, state clearly in the report that it must be **revoked and rotated immediately**.
