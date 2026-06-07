---
name: plan
description: Iterative plan-refinement loop. Draft and red-team an implementation plan before any code is written: up to 5 rounds, a fresh blind critic each round. Proposes only; never edits files. Called by /research-cycle Step 1, or run standalone.
---

# Plan

Refine a technical plan for the task through a draft → red-team → revise loop. Honor all
guardrails in GEMINI.md and AGENTS.md. This workflow proposes only — it NEVER edits the
tracker or source files.

## Step 0 — Context
1. Read `docs/PROJECT_TRACKER.md` (§2, §8–§10, plus §3/§5 relevant to the task) and
   `docs/LESSONS_LEARNED.md`. Cross-reference the task against recorded pitfalls.
2. State the task in one line and name the Q#/F#/D# it touches.

## Step 1 — Loop (max 5 rounds; stop on sign-off)
1. **Draft** step-by-step implementation changes with the owning agents
   (`python-simulation`, `cpp-engine`, ...).
2. **Red-team:** spawn a NEW, blind `critic` agent to attack the draft for
   algorithmic/memory risk, edge cases & initialization, C++ portability, and testing
   blindspots. (Optionally also spawn a blind `reviewer` for design/contract sanity.) The
   `auditor` is NOT used here — it gates finished work, not plans.
3. **Revise** to address material critiques. Repeat until sign-off or 5 rounds.
4. For any C++ change, state whether the Python reference needs a parallel update; for any
   Python change, state whether C++ parity is in scope. Never leave this implicit.

## Step 2 — Brief
Return a Final Brief: [Documentation Assessment (proposed §11/§12 entries),
Final Implementation Plan, Debate & Differences Summary, Subagent Assessment]. Do NOT
modify the tracker or source files. Hand the brief to the approval gate.
