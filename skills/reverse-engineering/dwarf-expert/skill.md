---
name: dwarf-expert
description: Provides expertise for analyzing DWARF debug information and understanding the DWARF standard (v3-v5). Triggers when understanding DWARF data, parsing DWARF files, answering DWARF questions, or working with code that processes DWARF.
allowed-tools: Read Bash Grep Glob WebSearch
---

# DWARF Expert

Technical knowledge and expertise about the DWARF standard and how to interact with DWARF debug information.

## When to Use

- Understanding or parsing DWARF debug information from compiled binaries
- Answering questions about the DWARF standard (v3, v4, v5)
- Writing or reviewing code that interacts with DWARF data
- Using `dwarfdump` or `readelf` to extract debug information
- Verifying DWARF data integrity with `llvm-dwarfdump --verify`
- Working with DWARF parsing libraries (libdwarf, pyelftools, gimli, etc.)

## When NOT to Use

- **DWARF v1/v2**: Expertise limited to versions 3, 4, and 5
- **General ELF parsing**: Use standard ELF tools if DWARF data isn't needed
- **Executable debugging**: Use gdb/lldb for runtime behavior
- **Binary reverse engineering**: Use Ghidra/IDA unless analyzing DWARF sections specifically
- **Compiler debugging**: DWARF generation issues are compiler-specific

## Authoritative Sources

1. **Official DWARF Standards** (dwarfstd.org): Search "DWARF5 DW_TAG_subprogram site:dwarfstd.org"
2. **LLVM DWARF Implementation** (`llvm/lib/DebugInfo/DWARF/`):
   - `DWARFDie.cpp` — DIE handling and attribute access
   - `DWARFUnit.cpp` — Compilation unit parsing
   - `DWARFDebugLine.cpp` — Line number information
3. **libdwarf** (github.com/davea42/libdwarf-code): Reference C implementation

## Verification Workflows

```bash
# Structural validation
llvm-dwarfdump --verify <binary>
llvm-dwarfdump --verify --error-display=full <binary>
llvm-dwarfdump --verify --verify-json=errors.json <binary>

# Quality metrics
llvm-dwarfdump --statistics <binary>
```

## Choosing Your Approach

- **Verify DWARF integrity** → `llvm-dwarfdump --verify`
- **Answer standard questions** → Search dwarfstd.org or LLVM source
- **Simple section dump / general ELF** → Use `readelf` — see [readelf.md](references/readelf.md)
- **Parse/search/dump DWARF DIE nodes** → Use `dwarfdump` — see [dwarfdump.md](references/dwarfdump.md)
- **Write/review code for DWARF** → See [coding.md](references/coding.md)

## Key DWARF Concepts

### DIE (Debug Information Entry)
The fundamental unit of DWARF. Every DIE has a tag (`DW_TAG_*`) and attributes (`DW_AT_*`).

```
DW_TAG_subprogram
  DW_AT_name: "my_function"
  DW_AT_low_pc: 0x1234
  DW_AT_high_pc: 0x1280
  DW_AT_type: <reference to return type DIE>
```

### DWARF Sections

| Section | Purpose |
|---------|---------|
| `.debug_info` | Main DIE tree |
| `.debug_abbrev` | Abbreviation table for `.debug_info` |
| `.debug_line` | Line number table |
| `.debug_str` | String pool |
| `.debug_loc` | Location expressions |
| `.debug_ranges` | Non-contiguous address ranges |

### Reference Files

- [dwarfdump.md](references/dwarfdump.md) — dwarfdump command reference
- [readelf.md](references/readelf.md) — readelf command reference
- [coding.md](references/coding.md) — Writing code that processes DWARF
