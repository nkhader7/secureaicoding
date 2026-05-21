---
name: codeql
description: CodeQL security vulnerability scanning with interprocedural data flow and taint tracking. Use when performing deep security analysis on Java, Python, JavaScript, C/C++, Go, Ruby, or Swift codebases.
allowed-tools: Bash Read Write Glob Grep WebFetch
---

# CodeQL Security Analysis

Comprehensive CodeQL security scanning with interprocedural data flow and taint tracking analysis.

## When to Use

- Deep security analysis requiring data flow across function boundaries
- Finding injection vulnerabilities (SQL, XSS, command injection)
- Auditing authentication and authorization logic
- Verifying custom framework sinks and sources
- When Semgrep pattern matching is insufficient for complex data flow

## When NOT to Use

- Quick syntactic checks (use Semgrep instead)
- Languages not supported by CodeQL
- When no build system is available for compiled languages (try `build-mode=none` first)

## Core Principles (Non-Negotiable)

1. **Database quality validation**: A database that builds is not automatically good. Always assess file counts, baseline lines of code, and extractor errors.
2. **Data extensions are essential**: Standard frameworks (Django, Spring, Express) contain custom wrappers that CodeQL misses without explicit models.
3. **Explicit suite references prevent silent filtering**: Never pass pack names directly; generate custom `.qls` suite files.
4. **Zero findings require investigation**: No findings can mean poor database quality, not clean code.
5. **Platform-specific workarounds**: macOS Apple Silicon exit code 137 indicates arm64 mismatch, not a build failure.

## Three-Phase Workflow

### Phase 1: build-database
- Create CodeQL database using build methods in sequence
- Store artifacts in `$OUTPUT_DIR`

### Phase 2: create-data-extensions
- Detect or generate custom source/sink models
- Ensures custom frameworks are analyzed

### Phase 3: run-analysis
- Select rulesets, execute queries
- Include Trail of Bits and Community Packs
- Preserve unfiltered results

## Output Structure

```
$OUTPUT_DIR/
├── database/           # CodeQL database
├── build-logs/         # Extractor output
├── diagnostics/        # Quality metrics
├── extensions/         # Custom data models
└── results/            # SARIF output
```

## Key Rejection Points

These shortcuts lead to incomplete analysis:

- Assuming "security-extended is enough" without Trail of Bits or Community Packs
- Claiming "security-and-quality covers all cases" while excluding experimental queries
- Treating successful database builds as proof of extraction quality
- Skipping data extensions for standard frameworks
- Using `build-mode=none` for compiled languages without attempting alternatives
- Reporting zero findings without investigation

## Validation Checklist

Complete analysis requires:
- [ ] Output directory resolved
- [ ] Database quality assessed (file count, LOC, extractor errors)
- [ ] Data extensions evaluated
- [ ] Explicit suite references (`.qls` files, not pack names)
- [ ] Comprehensive query pack inclusion (including Trail of Bits packs)
- [ ] Unfiltered results preserved
- [ ] Zero-finding scenarios investigated
