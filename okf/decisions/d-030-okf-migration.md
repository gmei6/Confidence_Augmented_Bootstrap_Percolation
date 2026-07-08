---
type: Decision
title: "D-030: Migrate tracker + lessons into the okf/ knowledge bundle"
description: "Tracker and lessons migrated into the okf/ knowledge bundle with zero information loss."
mutability: append-only
timestamp: 2026-07-04
---

# D-030: Migrate tracker + lessons into the okf/ knowledge bundle

Decision: replace the single-file `docs/PROJECT_TRACKER.md` + `docs/LESSONS_LEARNED.md` memory scheme with the `okf/` knowledge bundle (per queue task I), mirroring the structure and conventions of the sibling `project_template` reference implementation, with zero information loss.

Rationale: one file per concept with explicit `mutability` frontmatter (`frozen` / `live` / `append-only`) replaces the tracker's 🔒/🟢/📜 legend with a machine-checkable convention; per-entry decision/change files make the append-only record tamper-evident (locked `chmod 444`, appended only via `append_okf.py`); session context loads token-efficiently via the `session-start` skill instead of pasting a 580-line tracker. The §0 canary protocol and §14 update protocol move into the `session-start` / `session-wrapup` skills; the §N section labels are preserved in the migrated files' headings so every existing cross-reference (`§5.4`, `§3.6`, ...) stays resolvable.

Affects: every tracker section §1–§13 (migrated), §0/§14 (folded into skills), `AGENTS.md` (pointers), `docs/PROJECT_TRACKER.md` and `docs/LESSONS_LEARNED.md` (retired to redirect stubs). Known gap carried over faithfully: tracker §12 had already elided entries S-011–S-018 (a literal `- ...` line); they are not recoverable and were not fabricated.
