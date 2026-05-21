---
name: building-secure-contracts
description: Security patterns, best practices, and common vulnerability guidance for smart contract development. Use when writing or reviewing Solidity, Vyper, or other smart contract code.
allowed-tools: Read Bash Glob Grep WebFetch
---

# Building Secure Contracts

Security patterns and best practices for smart contract development, covering common vulnerability classes and their mitigations.

## When to Use

- Writing new smart contracts
- Security review of existing contracts
- Onboarding developers to smart contract security
- Pre-audit preparation

## Core Vulnerability Classes

### Reentrancy
```solidity
// VULNERABLE: External call before state update
function withdraw(uint amount) external {
    require(balances[msg.sender] >= amount);
    (bool success,) = msg.sender.call{value: amount}("");  // callback can re-enter
    balances[msg.sender] -= amount;  // state updated after external call

// SAFE: Update state before external call (CEI pattern)
function withdraw(uint amount) external {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;  // state updated first
    (bool success,) = msg.sender.call{value: amount}("");
}
```

### Access Control
- Always check `msg.sender` for privileged operations
- Use OpenZeppelin's `Ownable`, `AccessControl`, or `AccessControlEnumerable`
- Avoid using `tx.origin` for authentication

### Integer Overflow/Underflow (pre-Solidity 0.8)
- Use Solidity 0.8+ (automatic overflow checks) or SafeMath library
- Be aware of unchecked blocks in Solidity 0.8+

### Front-Running
- Commit-reveal schemes for sensitive operations
- Use minimum/maximum slippage parameters
- Consider block.timestamp manipulation

### Oracle Manipulation
- Use multiple independent price oracles
- Use time-weighted average prices (TWAP)
- Avoid spot prices for critical calculations

### Flash Loan Attacks
- Reentrancy guards on all state-changing functions
- Validate state consistency at end of transactions
- Use OpenZeppelin's `ReentrancyGuard`

## Security Patterns

### Checks-Effects-Interactions (CEI)

```solidity
function action() external {
    // 1. CHECKS: Validate inputs and state
    require(condition, "Error message");
    
    // 2. EFFECTS: Update state
    state = newValue;
    
    // 3. INTERACTIONS: External calls last
    externalContract.call(...);
}
```

### Pull over Push

Prefer letting users withdraw funds rather than pushing funds to them:

```solidity
// PUSH (dangerous): You call external addresses
function distribute() external {
    for (address user : users) {
        user.call{value: amounts[user]}("");  // Any can block all
    }
}

// PULL (safe): Users call you
function withdraw() external {
    uint amount = balances[msg.sender];
    balances[msg.sender] = 0;
    msg.sender.call{value: amount}("");
}
```

## Recommended Libraries

- [OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-contracts): Battle-tested implementations
- [solmate](https://github.com/transmissions11/solmate): Gas-optimized implementations

## Testing Requirements

- Unit tests for all access control paths
- Fuzzing for arithmetic operations
- Fork testing against mainnet state
- Property-based testing for invariants (use `building-secure-contracts` + `property-based-testing` skills)
