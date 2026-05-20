---
name: ask-questions-if-underspecified
description: Pauses to ask clarifying questions when task requirements are unclear or underspecified. Use before starting work that would be wrong or wasteful without more information.
allowed-tools: AskUserQuestion
---

# Ask Questions If Underspecified

Pause and ask the minimum set of clarifying questions needed to avoid wrong work before starting implementation.

## Core Principle

**Do not start implementing until must-have questions are answered.**

Ask only the questions where answering them incorrectly would waste significant work or produce a wrong outcome.

## When to Ask

Treat requests as needing clarification when details are missing for:

- **Objective**: What does success look like? What's the goal?
- **Completion criteria**: When is it done? What does "done" mean?
- **Scope**: Which files, systems, or components are in scope?
- **Constraints**: Any limitations (time, tech stack, compatibility, style)?
- **Environment**: Where does this run? What's the deployment context?
- **Safety/Reversibility**: Are there irreversible actions to confirm?

## When NOT to Ask

Don't ask questions that are:
- Answerable through quick, low-risk discovery (file reads, simple searches)
- Covered by reasonable defaults the user likely intends
- Answerable with a safe assumption that can be mentioned when reporting results

## Question Format

- Ask **1–5 targeted questions** in the first round
- Prefer **multiple-choice options** over open-ended questions
- **Mark the recommended/default choice** in bold
- Provide a **fast-path response** (e.g., "Reply `defaults` to use all defaults")
- Include a low-friction "not sure" option where appropriate

## Example Format

```
Before I begin, I need a few details:

1. **Target language**: Which language should I implement this in?
   - **Python (Recommended)**
   - TypeScript
   - Other (specify)

2. **Scope**: Which files are in scope?
   - **All files in src/ directory**
   - Only files you'll specify
   - Entire repository

3. **Output format**: Where should results go?
   - **Print to stdout**
   - Write to a file
   - Return as structured data

Reply `defaults` to use all recommended options, or answer any questions you want to customize.
```

## After Receiving Answers

Restate requirements before proceeding:

```
Based on your answers, I'll:
- Implement in Python
- Target all files in src/
- Print results to stdout

[Proceeding with implementation...]
```

## Rationalizations to Reject

- **"I'll figure it out as I go"** → Large changes in wrong direction waste both parties' time
- **"It's probably the obvious thing"** → When not obvious to you, ask; don't guess
- **"Asking seems annoying"** → Wrong work is more annoying than one question
