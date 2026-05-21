---
name: insecure-defaults
description: Detects fail-open vulnerabilities where applications operate insecurely due to missing configuration rather than explicit malicious code. Use during production security audits and pre-deployment checks.
allowed-tools: Bash Read Glob Grep
---

# Insecure Defaults Detection

Identifies **fail-open vulnerabilities** where applications operate insecurely due to missing configuration.

## Core Distinction

- **Fail-open (vulnerable):** `SECRET = env.get('KEY') or 'default'` — App functions with weak defaults
- **Fail-secure (safe):** `SECRET = env['KEY']` — App crashes if configuration is absent

## When to Use

- Production security audits (authentication, cryptography, API protection)
- Deployment file reviews (infrastructure-as-code, containerized configs)
- Code examination of secrets handling and environment variable patterns
- Pre-deployment validation for hardcoded credentials or permissive settings

## When NOT to Use

Skip analysis of:
- Test directories and fixtures
- Template/example files with `.example`, `.sample`, `.template` suffixes
- Development-only tooling
- Documentation samples
- Build-time configs replaced during deployment
- Fail-secure patterns where absence prevents execution

## Six Vulnerability Categories

1. **Fallback Secrets**: `env.get('KEY', 'default-secret')` — weak secret if env var missing
2. **Default Credentials**: Hardcoded admin accounts, API keys in code
3. **Fail-Open Security**: Auth disabled by default, CORS allows `*`, debug mode default true
4. **Weak Crypto**: MD5 for passwords, DES encryption, SHA1 for signatures
5. **Permissive Access**: World-writable files, public S3 buckets, CORS misconfiguration
6. **Debug Features**: Stack traces in API responses, GraphQL introspection in production

## Investigation Workflow

**Discovery Phase**: Search configuration directories and secrets management code for:
- Fallback patterns (`or 'default'`, `getOrDefault`, `||`)
- Hardcoded credentials
- Weak cryptographic defaults
- Insecure algorithm selections

**Verification Phase**: Trace execution paths to confirm:
- Does missing config cause crash (fail-secure) or permissive operation (fail-open)?
- Is this actually reachable in production code?

**Impact Assessment**: Determine if production environments rely on code-level defaults.

**Documentation**: Report with specific code locations, execution context, and exploitation scenarios.

## Reference

See [examples.md](references/examples.md) for patterns in Python, JavaScript, Ruby, Java across all six categories.

## Rationalizations to Reject

- **"It's only a development default"** → Development defaults that reach production code ARE vulnerabilities
- **"Production will override this"** → Verify with concrete evidence, not assumptions
- **"We'll fix it before deployment"** → Deployment slips happen; defaults persist
