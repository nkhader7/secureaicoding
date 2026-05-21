---
name: sarif-parsing
description: Parses, analyzes, and processes SARIF (Static Analysis Results Interchange Format) files from security tools. Use when reading scan results, aggregating findings from multiple tools, or integrating SARIF into CI/CD pipelines.
allowed-tools: Bash Read Write Glob Grep
---

# SARIF Parsing

Reads, analyzes, deduplicates, and processes SARIF 2.1.0 files from static analysis tools.

## When to Use

- Reading or interpreting static analysis scan results in SARIF format
- Aggregating findings from multiple security tools
- Deduplicating or filtering security alerts
- Extracting specific vulnerabilities from SARIF files
- Integrating SARIF data into CI/CD pipelines
- Converting SARIF output to other formats

## When NOT to Use

- Running static analysis scans (use `codeql` or `semgrep` skills)
- Writing CodeQL or Semgrep rules
- Analyzing source code directly without SARIF input

## SARIF Structure (2.1.0)

```
sarifLog
├── version: "2.1.0"
└── runs[]
    ├── tool.driver (name, version, rules[])
    ├── results[] (ruleId, level, message.text, locations[], fingerprints{})
    └── artifacts[]
```

## Tool Selection Guide

| Use Case | Tool | Installation |
|----------|------|--------------|
| Quick CLI queries | jq | `brew/apt install jq` |
| Python (simple) | pysarif | `pip install pysarif` |
| Python (advanced) | sarif-tools | `pip install sarif-tools` |
| Validation | SARIF Validator | sarifweb.azurewebsites.net |

## Quick Analysis with jq

```bash
# Count findings by severity
jq '[.runs[].results[]] | group_by(.level) | map({level: .[0].level, count: length})' results.sarif

# Extract all findings with locations
jq -r '.runs[].results[] | "\(.level) \(.ruleId) \(.locations[0].physicalLocation.artifactLocation.uri):\(.locations[0].physicalLocation.region.startLine)"' results.sarif

# Filter by severity
jq '.runs[].results[] | select(.level == "error")' results.sarif

# Get all rule IDs
jq -r '[.runs[].results[].ruleId] | unique[]' results.sarif
```

## Python with pysarif

```python
from pysarif import load_from_file

sarif_log = load_from_file("results.sarif")
for run in sarif_log.runs:
    for result in run.results:
        location = result.locations[0].physical_location
        print(f"{result.level}: {result.rule_id} @ {location.artifact_location.uri}:{location.region.start_line}")
```

## Aggregating Multiple SARIF Files

```python
import json

def merge_sarif_files(paths: list[str]) -> dict:
    merged = {"version": "2.1.0", "runs": []}
    for path in paths:
        with open(path) as f:
            sarif = json.load(f)
        merged["runs"].extend(sarif.get("runs", []))
    return merged
```

## Key Principles

1. **Validate first**: Use SARIF validator before processing
2. **Handle optionals**: Many fields may be absent; use defensive access
3. **Normalize paths**: Handle `file://` prefix, URL encoding, relative vs. absolute
4. **Fingerprint wisely**: Fingerprints may differ between environments
5. **Stream large files**: Use `ijson` for files >100MB

## Common Pitfalls

1. **Path normalization**: `file:///home/user/file.py` vs `./file.py` — normalize before comparing
2. **Fingerprint mismatch**: Same finding may have different fingerprints across CI environments
3. **Missing data**: `result.locations` may be empty; check before accessing
4. **Large files**: Don't load 100MB+ SARIF into memory; use streaming

## CI/CD Integration

```yaml
# GitHub Actions: Upload SARIF to Code Scanning
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif

# Fail on new issues (using sarif-tools)
- run: |
    pip install sarif-tools
    sarif diff --old baseline.sarif --new current.sarif --check-new-issues
```
