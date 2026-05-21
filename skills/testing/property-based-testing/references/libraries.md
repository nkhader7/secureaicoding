# Property-Based Testing Libraries by Language

## Python

### Hypothesis (Recommended)
```bash
pip install hypothesis
```

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s

@given(st.lists(st.integers()))
def test_sort_is_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)
```

**Key strategies**: `st.text()`, `st.integers()`, `st.lists()`, `st.dictionaries()`, `st.binary()`, `st.floats()`

**Custom strategies**:
```python
from hypothesis import strategies as st

valid_user = st.fixed_dictionaries({
    'name': st.text(min_size=1, max_size=50),
    'age': st.integers(min_value=0, max_value=150),
})
```

---

## JavaScript/TypeScript

### fast-check (Recommended)
```bash
npm install fast-check
```

```typescript
import * as fc from 'fast-check';

test('decode inverts encode', () => {
  fc.assert(
    fc.property(fc.string(), (s) => {
      expect(decode(encode(s))).toBe(s);
    })
  );
});
```

**Key arbitraries**: `fc.string()`, `fc.integer()`, `fc.array()`, `fc.record()`, `fc.oneof()`

---

## Rust

### proptest (Recommended)
```toml
[dev-dependencies]
proptest = "1"
```

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn decode_inverts_encode(s in ".*") {
        let encoded = encode(&s);
        let decoded = decode(&encoded).unwrap();
        prop_assert_eq!(decoded, s);
    }
}
```

### Arbitrary crate
```rust
use arbitrary::Arbitrary;

#[derive(Arbitrary, Debug)]
struct Config { value: u32, name: String }
```

---

## Haskell

### QuickCheck (Original PBT library)
```haskell
import Test.QuickCheck

prop_encode_decode :: String -> Bool
prop_encode_decode s = decode (encode s) == s

main :: IO ()
main = quickCheck prop_encode_decode
```

---

## Go

### rapid (Recommended)
```bash
go get pgregory.net/rapid
```

```go
func TestDecodeInvertsEncode(t *testing.T) {
    rapid.Check(t, func(t *rapid.T) {
        s := rapid.StringOf(rapid.Rune()).Draw(t, "s").(string)
        require.Equal(t, s, decode(encode(s)))
    })
}
```

---

## Java/Kotlin

### jqwik (Recommended)
```xml
<dependency>
    <groupId>net.jqwik</groupId>
    <artifactId>jqwik</artifactId>
    <version>1.7.4</version>
    <scope>test</scope>
</dependency>
```

```java
@Property
void decodeInvertsEncode(@ForAll String s) {
    assertThat(decode(encode(s))).isEqualTo(s);
}
```

---

## Smart Contracts

### Echidna (Solidity fuzzing)
```solidity
// echidna_test.sol
contract EchidnaTest {
    Token token;
    
    constructor() {
        token = new Token(1000000);
    }
    
    // Echidna will try to violate this
    function echidna_balance_invariant() public view returns (bool) {
        return token.totalSupply() == 1000000;
    }
}
```

```bash
echidna ./contracts/ --contract EchidnaTest --config echidna.yaml
```

### Foundry (Property-based tests)
```solidity
contract TokenTest is Test {
    function testFuzz_transferDoesNotChangeTotal(
        address from,
        address to,
        uint256 amount
    ) public {
        vm.assume(from != to);
        vm.assume(balanceOf(from) >= amount);
        uint256 totalBefore = totalSupply();
        transfer(from, to, amount);
        assertEq(totalSupply(), totalBefore);
    }
}
```

---

## Choosing a Library

| Language | Recommended | Alternative |
|----------|-------------|-------------|
| Python | Hypothesis | pytest-quickcheck |
| JavaScript | fast-check | jsverify |
| TypeScript | fast-check | — |
| Rust | proptest | quickcheck |
| Go | rapid | gopter |
| Haskell | QuickCheck | hedgehog |
| Java | jqwik | QuickTheories |
| Kotlin | kotest-property | — |
| Solidity | Echidna + Foundry | Medusa |
