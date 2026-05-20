# Zeroize Detection Strategy

A 12-step methodology for identifying zeroization failures in cryptographic code, divided into two phases.

## Phase 1: Source-Level Analysis (Steps 1–6)

### Step 1: Preflight Check
Verify the compile database exists and the codebase compiles. Analysis requires valid build artifacts:
- C/C++: `compile_commands.json`
- Rust: buildable `Cargo.toml`

### Step 2: Identify Sensitive Objects

Three confidence levels for identifying secrets:

**Low confidence** — Name pattern matching:
```
"key", "secret", "seed", "token", "password", "credential", "private", "nonce"
```

**Medium confidence** — Type hints:
- Byte buffers and arrays (`[u8; N]`, `Vec<u8>`, `uint8_t[]`)
- Custom types with cryptographic names

**High confidence** — Explicit annotations:
```rust
#[secret]                                    // Rust custom annotation
__attribute__((annotate("sensitive")))       // C/C++ attribute
```

### Step 3: Check for Zeroization Attempts

For each sensitive object, check if an approved wipe API is called before the object goes out of scope.

**Approved C/C++ APIs:**
- `explicit_bzero(ptr, size)` — OpenBSD/Linux, compiler-safe
- `memset_s(ptr, smax, c, n)` — C11, cannot be optimized away
- `SecureZeroMemory(ptr, size)` — Windows API
- `OPENSSL_cleanse(ptr, size)` — OpenSSL
- `sodium_memzero(ptr, size)` — libsodium
- Volatile wipe loops: `for (size_t i = 0; i < n; i++) ((volatile uint8_t*)p)[i] = 0;`

**Approved Rust APIs:**
- `zeroize::Zeroize::zeroize()` — zeroize crate
- `Zeroizing<T>` wrapper — automatic zeroize on drop
- `#[derive(ZeroizeOnDrop)]` macro

**NOT approved:**
- `memset()` — can be eliminated by dead-store elimination
- Manual `bzero()` — no guarantee of non-optimization

### Step 4: MCP Semantic Pass

Resolve symbol names and trace cleanup paths across multiple files. Identify:
- Functions that receive pointers to sensitive data
- Copy operations that create unsanitized duplicates
- Error paths that bypass cleanup

### Step 5: Validate Correctness

For each zeroization attempt:
1. **Wipe size**: Does it cover the entire sensitive buffer?
2. **Exit path coverage**: Is wipe called on ALL exit paths (normal return, error, exception)?
3. **Pre-free ordering**: Does wipe happen BEFORE `free()`/deallocation?

### Step 6: Source Analysis Summary

Compile findings with confidence levels:
- `confirmed`: wipe missing, wipe incomplete, or wipe potentially optimized
- `likely`: wipe present but ordering or coverage questionable
- `needs_review`: name patterns matched but no semantic verification done

---

## Phase 2: Compiler-Level Analysis (Steps 7–12)

**Prerequisite**: Valid compilation infrastructure from Phase 1.

### Step 7: IR Comparison

Detect when zeroization is optimized away by comparing LLVM IR across optimization levels:

```bash
# C/C++: Generate IR at different optimization levels
clang -O0 -emit-llvm -S -o file_O0.ll file.c
clang -O1 -emit-llvm -S -o file_O1.ll file.c
clang -O2 -emit-llvm -S -o file_O2.ll file.c

# Diff to find eliminated zeroization
diff file_O0.ll file_O2.ll | grep -A5 "memset\|bzero\|zeroize"
```

If the wipe call appears at O0 but disappears at O1/O2, it was optimized away → confirmed vulnerability.

### Step 8: Assembly Analysis

Inspect compiled assembly for:
- Register spills of sensitive values onto the stack after use
- Stack frames not zeroed before `ret`
- Sensitive values in callee-saved registers

```bash
# Disassemble relevant function
objdump -d -M intel binary | grep -A100 "<sensitive_func>"
gdb binary -ex "disas sensitive_func" -ex quit
```

### Step 9: Semantic IR Analysis

Verify loop-unrolled wipe patterns cover the full object size. Some compilers unroll `for` loops — check that all bytes are covered.

### Step 10: CFG Analysis

Confirm wipe operations **dominate** all exit paths:
- Normal return paths
- Early return on error
- Exception handling paths (C++ `throw`)
- Panic paths (Rust `unwrap`, `expect`)

A wipe that only appears on the happy path is incomplete.

### Step 11: Runtime Test Generation

Create test harnesses with sanitizers that detect secret retention:
```c
// Compile with: -fsanitize=address -fsanitize=memory
// Run under valgrind: valgrind --tool=memcheck --track-origins=yes
```

### Step 12: PoC Generation

For each confirmed finding, produce a proof-of-concept that:
- Compiles and executes
- Demonstrates exploitability (e.g., reads stack memory after function returns)
- Includes compiler evidence (IR/assembly diffs)

---

## Confidence Mapping

| Evidence | Confidence |
|----------|-----------|
| Source pattern only (name match) | `needs_review` |
| Source pattern + missing wipe call | `likely` |
| Source analysis + IR shows DSE | `confirmed` |
| Source analysis + assembly shows stack retention | `confirmed` |
| IR analysis + assembly corroboration | `confirmed` |

**Rule**: `confirmed` requires minimum 2 independent evidence signals. Hard evidence (compiler elimination, assembly artifacts) cannot be waived for `confirmed` status.
