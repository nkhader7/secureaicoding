# Security Audit Report

## Summary
- **Skill**: {{skill_name}}
- **Scan scope**: {{scan_scope}}
- **Files scanned**: {{files_scanned}}
- **Rules evaluated**: {{rules_evaluated}}
- **Execution mode**: {{execution_mode}}

## Findings by Severity
- **Critical**: {{count_critical}}
- **High**: {{count_high}}
- **Medium**: {{count_medium}}
- **Low**: {{count_low}}
- **Info**: {{count_info}}

## Findings
{{#findings}}
### {{id}} — {{name}}
- **Severity**: {{severity}}
- **Confidence**: {{confidence}}
- **File**: `{{file}}`
- **Line**: {{line}}
- **Rule reference**: {{rule_ref}}
- **Remediation**: {{remediation}}

**Evidence (with context):**
```text
{{context_snippet}}
```
{{/findings}}

## Performance Notes
- **Cache hits**: {{cache_hits}}
- **Cache misses**: {{cache_misses}}
- **Rules skipped by file type pre-filter**: {{rules_skipped_file_type}}
- **Lines skipped by min_line_length**: {{lines_skipped_min_length}}
- **Lines skipped as comments**: {{lines_skipped_comments}}
- **Files skipped by max_file_size_kb**: {{files_skipped_size}}
- **Hybrid fallback invocations**: {{hybrid_fallback_invocations}}

## Recommendations
1. Prioritize Critical/High findings first.
2. Move secrets to a secrets manager or environment variables.
3. Add regression checks for fixed findings.
