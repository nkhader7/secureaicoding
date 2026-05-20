# Mutation Testing Optimization Strategies

Apply these strategies **before** running a campaign when the estimated duration exceeds 16 hours or the user requests optimization.

## Priority 1: Verify Target Selection

**Most common issue:** Mutating non-source code.

```bash
mewt print config     # Check [targets] include/ignore
mewt print targets    # Check what was actually mutated
```

**Look for unintended files:**
- Mocks: `src/mocks/`, `__mocks__/`
- Tests: `*_test.rs`, `*.test.js`, `tests/`
- Dependencies: `vendor/`, `node_modules/`
- Generated: `proto/`, `generated/`

**Fix:**
```toml
# Before (too broad)
[targets]
include = ["**/*.rs"]

# After (specific)
[targets]
include = ["src/**/*.rs", "lib/**/*.rs"]
ignore = ["test", "mock", "generated"]
```

After editing, re-run `mewt mutate` and check new count.

## Priority 2: Analyze Project Structure

Get mutant distribution to estimate duration:

```bash
mewt print mutants --target 'src/auth/**/*.rs' | wc -l
mewt print mutants --severity high | wc -l
mewt print mutants --severity medium | wc -l
mewt status
```

Present breakdown to user:
```
Component breakdown:
- src/auth/: 200 mutants × 5s = ~17 min
- src/core/: 800 mutants × 8s = ~1.8 hrs
Total: 1000 mutants, ~2 hrs worst-case
```

## Priority 3: Choose Optimization Approach

### Option A: Run Full Campaign
- Present time estimate
- Recommend when duration is acceptable and comprehensive coverage is desired

### Option B: Target Critical Components
```toml
[targets]
include = ["src/auth/**/*.rs"]  # Start with critical component
```

After editing: `mewt purge && mewt mutate src/ && mewt status`

### Option C: High/Medium Severity Only
```toml
[run]
mutations = ["ER", "CR", "IF", "IT"]  # High/medium severity types
```

After editing: `mewt purge --all && mewt mutate src/ && mewt status`

Or use severity filtering during analysis (no database changes):
```bash
mewt results --severity high,medium
```

### Option D: Two-Phase Campaign (Integration-Heavy Only)

Use ONLY when integration tests dominate runtime and unit tests don't map cleanly to files.

**Phase 1 config (targeted tests):**
```toml
[[test.per_target]]
glob = "src/auth/*.rs"
cmd = "cargo test auth::unit"
timeout = 10

[[test.per_target]]
glob = "src/core/*.rs"
cmd = "cargo test core::unit"
timeout = 15

# Catch-all: full suite for unmatched files
[[test.per_target]]
glob = "**/*.rs"
cmd = "cargo test"
timeout = 60
```

**Run Phase 1:**
```bash
mewt run
```

**Phase 2 (after Phase 1 completes):**
```bash
# Extract uncaught mutants
mewt results --status Uncaught --format ids > uncaught_ids.txt

# Update mewt.toml: comment out all [[test.per_target]], uncomment [test]
# [test]
# cmd = "cargo test"
# timeout = 60

# Re-test with full suite
mewt test --ids-file uncaught_ids.txt
```

**Typical speedup:**
```
Naive:       2,000 mutants × 45s = 25 hours
Two-phase:   Phase 1: 2,000 × 8s = 4.4h → 450 uncaught
             Phase 2: 450 × 45s = 5.6h → 180 truly uncaught
Total: ~10 hours (2.5× speedup)
```

**Note**: Phase 2 duration is unknown until Phase 1 completes.

## Per-Target Test Configuration

Use when tests are well-organized by module and targeted tests are significantly faster.

```toml
[test]
cmd = "go test ./..."
timeout = 45

[[test.per_target]]
glob = "auth/*.go"
cmd = "go test ./auth"
timeout = 10

[[test.per_target]]
glob = "core/*.go"
cmd = "go test ./core"
timeout = 15

# Catch-all for unmatched files
[[test.per_target]]
glob = "*.go"
cmd = "go test ./..."
timeout = 45
```

**Ordering matters**: First match wins. Most specific patterns first, catch-all last.

**Verify speedup before committing**:
```bash
time go test ./...     # Full suite
time go test ./auth    # Targeted
```

If targeted tests aren't significantly faster, this optimization won't help.
