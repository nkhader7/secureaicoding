---
name: burpsuite-project-parser
description: Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers/bodies, extracting security audit findings, or analyzing HTTP traffic captured in a Burp project.
allowed-tools: Bash Read
---

# Burp Suite Project Parser

Search and extract data from Burp Suite project files using the burpsuite-project-file-parser extension.

## When to Use

- Searching response headers or bodies with regex patterns
- Extracting security audit findings from Burp projects
- Dumping proxy history or site map data
- Analyzing HTTP traffic captured in a Burp project file

## Prerequisites

1. **Burp Suite Professional**
2. **burpsuite-project-file-parser extension** from `github.com/BuffaloWill/burpsuite-project-file-parser`

## Quick Reference

```bash
scripts/burp-search.sh /path/to/project.burp [FLAGS]
```

Environment variables: `BURP_JAVA`, `BURP_JAR`

## Sub-Component Filters (Use These)

| Filter | Returns | Typical Size |
|--------|---------|--------------|
| `proxyHistory.request.headers` | Request line + headers only | Small |
| `proxyHistory.request.body` | Request body only | Variable |
| `proxyHistory.response.headers` | Status + headers only | Small |
| `proxyHistory.response.body` | Response body only | **LARGE — avoid** |
| `siteMap.request.headers` | Same for site map | Small |
| `siteMap.response.body` | — | **LARGE — avoid** |

**HARD RULE: Body content > 1000 chars must NEVER enter context.**

## Regex Search Operations

```bash
# Search response headers
scripts/burp-search.sh project.burp responseHeader='.*X-Content-Type-Options.*'

# Search response bodies (always truncate)
scripts/burp-search.sh project.burp responseBody='.*password.*' | head -c 1000
```

## Other Operations

```bash
# Get all security findings
scripts/burp-search.sh project.burp auditItems

# Get proxy history (USE SUB-COMPONENT FILTERS)
# NEVER: scripts/burp-search.sh project.burp proxyHistory
# DO:    scripts/burp-search.sh project.burp proxyHistory.request.headers
```

## Output Limits (Required)

Always check result size BEFORE retrieving data:
```bash
scripts/burp-search.sh project.burp proxyHistory.request.headers | wc -cl
```

| Metric | Safe | Narrow | Too Broad | STOP |
|--------|------|--------|-----------|------|
| Lines | <50 | 50–200 | 200+ | 1000+ |
| Bytes | <50KB | 50–200KB | 200KB+ | 1MB+ |

## Severity vs. Confidence

| Combination | Meaning |
|-------------|---------|
| High + Certain | Likely real vulnerability |
| High + Tentative | Often a false positive |
| Medium + Firm | Worth investigating |
| Low + Certain | Informational, low priority |

## Platform Configuration

```bash
# macOS
export BURP_JAVA="/Applications/Burp Suite Professional.app/Contents/Resources/jre.bundle/Contents/Home/bin/java"

# Linux
export BURP_JAVA="/opt/BurpSuiteProfessional/jre/bin/java"

# Windows (PowerShell)
$env:BURP_JAVA = "C:\Program Files\BurpSuiteProfessional\jre\bin\java.exe"
```

## Rationalizations to Reject

- **"This regex looks good"** → Verify on sample data first — encoding and escaping cause silent failures
- **"High severity = must fix"** → Check confidence score too; High + Tentative is often a false positive
- **"All audit items are relevant"** → Filter by actual threat model
- **"Burp found it, so it's a vulnerability"** → All Burp findings require manual verification
