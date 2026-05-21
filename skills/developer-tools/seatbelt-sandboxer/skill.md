---
name: seatbelt-sandboxer
description: Generates minimal allowlist-based macOS Seatbelt sandbox configurations to restrict application permissions. Use when sandboxing processes for security isolation or supply chain attack defense.
allowed-tools: Bash Read Write Edit
---

# Seatbelt Sandboxer

Generates minimal, allowlist-based macOS Seatbelt sandbox configurations (`sandbox-exec` profiles) to restrict application permissions.

## When to Use

- Sandboxing untrusted processes (supply chain attack defense)
- Restricting application file system access
- Isolating development tools from sensitive system areas
- Creating defense-in-depth profiles for CI/CD runners

## When NOT to Use

- Linux systems (use seccomp/AppArmor instead)
- Applications requiring unrestricted system access
- Debugging sandbox escape issues (use Activity Monitor + Console.app)

## Platform Note

Apple deprecated `sandbox-exec` but it works through macOS 14+.

## Six-Step Profiling Methodology

### Step 1: Identify Resource Requirements
Determine what the application needs:
- Which files must it read?
- Which directories must it write?
- Does it need network access?
- Does it need to spawn subprocesses?

### Step 2: Start with Deny-All Baseline

```scheme
(version 1)
(deny default)
(allow process-exec)
(allow process-fork)
(allow signal (target self))
```

### Step 3: Add File Read Access

Use `file-read-data` (not wildcards) for specific paths:

```scheme
; Allow reading specific directories
(allow file-read-data
  (subpath "/usr/lib")
  (subpath "/usr/share")
  (literal "/etc/resolv.conf"))
```

### Step 4: Configure Restricted File Write Access

```scheme
; Allow writing to working directory and temp locations
(allow file-write-data
  (subpath "/tmp")
  (subpath (string-append (param "HOME") "/project")))
```

### Step 5: Set Network Policy

Choose one level:
```scheme
; Complete blocking (most restrictive)
; (no network rules — denied by default)

; Localhost only
(allow network-outbound
  (local ip "localhost:*"))

; Unrestricted (least restrictive)
(allow network-outbound)
(allow network-inbound)
```

### Step 6: Test Iteratively

```bash
# Run application in sandbox
sandbox-exec -f profile.sb /path/to/application

# Check for denied operations in Console.app
# Filter: "sandbox: deny"
```

Iterate until the application functions normally with minimal permissions.

## Critical Design Principle

Combined use of `file-read-metadata` (broad) and `file-read-data` (allowlist):

```scheme
; Can stat/readdir anywhere (needed for path resolution)
(allow file-read-metadata)

; Can only read CONTENTS of allowlisted files
(allow file-read-data
  (subpath "/usr/lib")
  (literal "/path/to/config.json"))
```

## Common Requirements

Most applications need at minimum:
```scheme
(allow file-read-metadata)          ; Path resolution
(allow file-read-data (subpath "/usr/lib"))   ; System libraries
(allow file-read-data (subpath "/System"))    ; macOS frameworks
(allow mach-lookup)                 ; macOS IPC
(allow sysctl-read)                 ; System information
```

## Practical Limitations

- `/tmp` and `/var/folders` are commonly required
- Some frameworks require Mach port access that is difficult to restrict
- File descriptor passing between processes may require additional rules
