---
name: let-fate-decide
description: Draws 4 Tarot cards using cryptographic randomness to inject entropy into planning when prompts are vague or casually delegated. Use when options are equivalent and a random choice is needed.
allowed-tools: Bash Read
---

# Let Fate Decide

Draws 4 Tarot cards using cryptographic randomness to inject entropy into planning when the user hasn't specified a preference and options are genuinely equivalent.

## When to Use

- User delegates a choice without specifying a preference
- Multiple options are genuinely equivalent and a random selection is acceptable
- Prompts are vague, ambiguous, or casually worded ("do whatever you think")
- Breaking a tie between two equally good approaches

## When NOT to Use

- User has a clear preference (even implied)
- The choice has significant security, performance, or correctness implications
- Domain expertise should guide the decision

## Core Rule

**Never fake entropy.** If the script cannot run (Python not available, cryptographic randomness unavailable), do NOT simulate a draw using internal "randomness." Tell the user the tool cannot run.

## How It Works

1. Run the Tarot draw script to generate 4 random cards using cryptographic randomness
2. Interpret the cards in context of the decision to be made
3. Map the interpretation to a specific choice
4. Proceed with that choice, noting it was fate-decided

## Interpretation Reference

See [INTERPRETATION_GUIDE.md](references/INTERPRETATION_GUIDE.md) for card meanings and interpretation frameworks.

## Example Usage

```
User: "Add some error handling to this function, whatever you think is best"

[fate draws: The Tower, The Wheel of Fortune, Page of Swords, Six of Pentacles]

The Tower → significant change/disruption → comprehensive error restructuring
The Wheel → cycles → wrap in retry logic
Page of Swords → investigation → add logging for debugging
Six of Pentacles → balance → proportional handling (not over-engineered)

Interpretation: Fate suggests a comprehensive retry-with-logging approach.
```
