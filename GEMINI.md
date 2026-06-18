# GEMINI.md — Antigravity-Specific Overrides

**Project: TwoCascade** — bootstrap-percolation / confidence-threshold cascade simulation.

> The shared constitution — invariants, persona, guardrails, the **§0 canary protocol**, and all `§N` references into `docs/PROJECT_TRACKER.md` — lives in **`AGENTS.md`**, which Antigravity loads natively alongside this file. **This file contains only Antigravity-specific mechanisms.** Where a rule here conflicts with `AGENTS.md`, this file wins (Antigravity precedence) — but everything here is written to *specialize* the constitution, never to weaken it.

---

## Agent Mode — the baseline-isolation mechanism

Implement the `AGENTS.md` baseline-isolation guardrail with **New Worktree Mode** for any change to `src/` or `cpp/src/`, so experimental changes can't corrupt the validation baseline. Use **Local Mode** only for documentation, config, or clearly-scoped single-file fixes that carry no cross-validation risk.

---

## Write-tool guardrail — the "propose, don't write" mechanism

The `AGENTS.md` "propose, don't write" rule applies specifically to the Antigravity writing tools — `write_to_file`, `replace_file_content`, and `multi_replace_file_content`. Present the diff or code block in chat and obtain explicit approval before any of these touch disk.

---

## Permissions — configure in the IDE, not in this file

Set these in **Agent Manager → Additional Options → Customizations → Permissions** to enforce the `AGENTS.md` permission policy. Do not manage them in this file.

| Action level | Guarded actions |
| --- | --- |
| **Always Ask** | `git commit`, `git push`, any file deletion |
| **Always Deny** | `git push --force`, `rm -rf`, direct writes to `results/` |

---

## Workflow

- **Primary entry:** `/research-cycle` — defined at `.agents/workflows/research-cycle.md`.
- **Verification:** the `/verify` workflow runs `reviewer → critic → auditor`, each spawned blind, each fed the preceding implementation session's `walkthrough.md`. The `auditor` returns a binary AUDIT PASS/FAIL — the mandatory gate before any result is marked done (see `AGENTS.md` §IV).
