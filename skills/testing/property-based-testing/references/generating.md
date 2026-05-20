# Generating Property-Based Tests

## Step 1: Identify Testable Properties

Before writing a single line of test code, identify what properties should hold.

### Common Property Sources

**From function signatures:**
```python
# encode: str -> bytes, decode: bytes -> str
# → Roundtrip: decode(encode(x)) == x
```

**From documentation:**
```
# "normalize() returns a canonical form"
# → Idempotence: normalize(normalize(x)) == normalize(x)
```

**From invariants:**
```
# "sum of all balances equals total supply"
# → Invariant: sum(balances.values()) == total_supply
```

## Step 2: Choose the Right Property

| Situation | Property |
|-----------|----------|
| encode/decode pair | Roundtrip |
| Normalization, formatting, sorting | Idempotence |
| Mathematical operations | Commutativity, Associativity |
| Optimization of known-good algorithm | Oracle |
| "Shouldn't crash" baseline | No Exception |

## Step 3: Write the Test

### Python (Hypothesis)

```python
from hypothesis import given, settings, strategies as st

# Roundtrip property
@given(st.text())
def test_roundtrip(s):
    assert decode(encode(s)) == s

# Idempotence property
@given(st.text())
def test_idempotence(s):
    assert normalize(normalize(s)) == normalize(s)

# Invariant property
@given(st.lists(st.integers(min_value=0, max_value=1000)))
def test_sum_preserved_after_sort(lst):
    assert sum(sorted(lst)) == sum(lst)
```

### TypeScript (fast-check)

```typescript
import * as fc from 'fast-check';

// Roundtrip property
test('roundtrip', () => {
  fc.assert(
    fc.property(fc.string(), (s) => {
      return decode(encode(s)) === s;
    })
  );
});

// Oracle property (compare against reference)
test('new implementation matches reference', () => {
  fc.assert(
    fc.property(fc.integer(), (n) => {
      return fastImpl(n) === referenceImpl(n);
    })
  );
});
```

## Step 4: Configure Generators

### Range Constraints

```python
# Hypothesis
st.integers(min_value=0, max_value=100)
st.text(min_size=1, max_size=255)
st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
```

### Composite Generators

```python
from hypothesis import strategies as st

# Nested structures
valid_address = st.fixed_dictionaries({
    'street': st.text(min_size=1),
    'city': st.text(min_size=1),
    'zip': st.from_regex(r'\d{5}'),
})

# Recursive structures
json_value = st.deferred(lambda: st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.text(),
    st.lists(json_value),
    st.dictionaries(st.text(), json_value),
))
```

### Filtering (Use Sparingly)

```python
# Slow: generates then discards
@given(st.integers().filter(lambda x: x % 2 == 0))

# Fast: generate even numbers directly
@given(st.integers().map(lambda x: x * 2))
```

## Step 5: Handle Failures

When a test fails, Hypothesis/fast-check will shrink the input to a minimal counterexample:

```
Falsifying example: test_roundtrip(s='\x00')
```

This is a **bug**, not a test issue:
1. Examine the minimal failing input
2. Reproduce with a regular unit test
3. Fix the underlying code
4. Verify the property test now passes

## Common Mistakes

- **Over-constraining generators**: Narrow constraints miss edge cases. Prefer wide inputs and use `assume()` only when needed.
- **Weak properties**: `assert result is not None` rarely finds bugs. Aim for stronger guarantees.
- **Missing edge cases**: Empty strings, empty lists, zero, negative numbers, None — generators should include these.
- **Ignoring shrinking**: The shrunk example reveals exactly what's wrong; don't debug the original input.
