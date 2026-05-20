---
name: yara-authoring
description: Authors and validates YARA rules for malware detection and threat hunting. Use when writing YARA signatures, building detection rules, or creating threat hunting queries.
allowed-tools: Bash Read Write Edit Glob Grep
---

# YARA Rule Authoring

Creates production-quality YARA rules for malware detection and threat hunting.

## When to Use

- Writing YARA rules for malware families
- Creating threat hunting rules for specific indicators
- Converting malware analysis findings into detection signatures
- Building detection coverage for known TTPs

## When NOT to Use

- Running existing YARA scans (use YARA directly)
- Threat intelligence enrichment without rule authoring

## YARA Rule Structure

```yara
rule MalwareFamilyName {
    meta:
        description = "Detects specific malware behavior"
        author = "Your Name"
        date = "2024-01-01"
        severity = "high"
        tlp = "white"
        
    strings:
        $string1 = "malicious_string" ascii wide
        $string2 = { 48 8B 45 F8 48 89 45 E8 }  // hex pattern
        $string3 = /regex_pattern[0-9]{4}/ ascii
        
    condition:
        uint16(0) == 0x5A4D and       // PE file
        filesize < 2MB and
        (2 of ($string*))
}
```

## String Modifiers

| Modifier | Purpose |
|----------|---------|
| `ascii` | Match ASCII encoding (default) |
| `wide` | Match UTF-16LE encoding |
| `nocase` | Case-insensitive match |
| `fullword` | Match only as complete word |
| `xor` | Match XOR-obfuscated variants |
| `base64` | Match base64-encoded variants |

## Condition Building

### File Type Checks
```yara
uint16(0) == 0x5A4D      // PE (MZ header)
uint16(0) == 0x457F      // ELF
uint32(0) == 0xFEEDFACE  // Mach-O (32-bit)
uint32(0) == 0xCEFAEDFE  // Mach-O (32-bit, reversed)
```

### String Combination Logic
```yara
condition:
    all of ($string*)          // All strings must match
    any of ($string*)          // Any string must match
    2 of ($string*)            // At least 2 must match
    ($str1 and $str2) or $str3 // Boolean logic
    $str1 at 0x100             // String at specific offset
    $str1 in (0..0x1000)       // String within range
```

### Performance-Aware Conditions
```yara
condition:
    // Check cheap conditions first
    filesize < 5MB and
    uint16(0) == 0x5A4D and   // PE check is fast
    any of them               // String scan is expensive; run last
```

## Reducing False Positives

1. **Add file type checks**: Reduce scope to expected file types
2. **Use `fullword` modifier**: Avoid substring matches
3. **Combine multiple indicators**: Require 2+ independent signals
4. **Test against known-good corpora**: Verify no FPs on clean files
5. **Add context conditions**: Require co-occurrence of related indicators

## Testing

```bash
# Test rule against known samples
yara rule.yar /path/to/samples/

# Test for false positives
yara rule.yar /path/to/clean/files/

# Verbose output
yara -s rule.yar sample.exe  # Show matching strings

# Compile and validate
yarac rule.yar rule.yarc
```

## Rationalizations to Reject

- **"One string is enough"** → Single generic strings produce high false positive rates; require multiple independent indicators
- **"Regex is more flexible"** → Regex scans are slow; use hex patterns or specific strings where possible
- **"I'll test it later"** → Test against both malicious samples and clean files before deploying
