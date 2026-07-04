# Task I — Migrate PROJECT_TRACKER / LESSONS_LEARNED into an OKF knowledge bundle

**One-line task.** Replace the single-file `docs/PROJECT_TRACKER.md` + `docs/LESSONS_LEARNED.md` memory scheme with an `okf/` knowledge bundle, mirroring the structure and conventions used in the sibling `project_template` repo, with zero information loss.

**Touches:** `docs/PROJECT_TRACKER.md`, `docs/LESSONS_LEARNED.md`, `AGENTS.md`, `CLAUDE.md` (pointer only), new `okf/` tree, new `.agents/skills/edit-okf/`, `.agents/skills/session-start/`, `.agents/skills/session-wrapup/`.

## Environment note (read first)

This container has **no git access**, on purpose. Do all work as plain file edits in the working tree. Do **not** attempt `git commit`, `git push`, `git branch`, or `git worktree` — those commands are expected to fail or must not be tried. This task is docs/config-only and does not touch `src/`, `cpp/`, `tests/`, `results/`, `viz/`, or `section2-reformulation/`, so the AGENTS.md "New Worktree Mode" isolation rule for `src/`/`cpp/src/` changes does not apply — edit in place. A human will review and commit the resulting working-tree diff afterward.

## Why this is low-human-input

Purely mechanical restructuring of existing, already-written content — no new research, no new code, no simulation runs. The hard part (deciding what OKF's conventions are) is already solved by the reference implementation at `../project_template/okf/` and its `.agents/skills/edit-okf/SKILL.md` — read both before starting, and copy their conventions exactly rather than reinventing them.

## Reference implementation

Read these from the sibling project before writing anything:
- `../project_template/okf/index.md` and every file it links to, to see the target shape (`identity.md`, `north-star.md`, `status.md`, `next-actions.md`, `open-questions.md`, `log.md`, `roadmap.md`, `risks.md`, `benchmark.md`, `architecture/`, `model/`, `references/`, `decisions/`, `changes/`).
- `../project_template/.agents/skills/edit-okf/SKILL.md` and `.../scripts/append_okf.py` — the mutability rules (`frozen` / `live` / `append-only`) and the append-only enforcement mechanism.
- `../project_template/.agents/skills/session-start/SKILL.md` and `.../session-wrapup/SKILL.md`.
- `../project_template/okf_skill_plan.md` for the rationale behind each convention.

## Plan

1. **Scaffold `okf/`** at the repo root with an `index.md` (frontmatter `mutability: live`, `type: index`; flat bullet list of links, no prose — copy the exact format from the reference).

2. **Migrate `docs/PROJECT_TRACKER.md` section-by-section.** Use this mapping (adjust only if the reference implementation's actual conventions clearly demand it):

   | Tracker section | OKF destination | mutability |
   |---|---|---|
   | §0 (session-start checklist, canary protocol) | fold into `.agents/skills/session-start/SKILL.md` (new, adapted from the reference) — not a content file | n/a |
   | §1 Project Identity | `okf/identity.md` | frozen |
   | §2 North Star & Contribution Claim | `okf/north-star.md` | frozen |
   | §3 Model Specification (3.1–3.6) | `okf/model/network-and-channels.md` (3.1–3.4), `okf/model/notation-and-parameters.md` (3.5), `okf/model/forks.md` (3.6), plus `okf/model/index.md` | frozen |
   | §4 Analytical Benchmark | `okf/benchmark.md` | frozen |
   | §5 Coding Standards & Architecture (5.1–5.6) | `okf/architecture/stack.md` (5.1–5.2), `okf/architecture/repo-layout.md` (5.3), `okf/architecture/reproducibility.md` (5.4), `okf/architecture/style.md` (5.5, new — the reference doesn't have this file; add it, it's a clean fit), `okf/architecture/definition-of-done.md` (5.6), plus `okf/architecture/index.md` | frozen |
   | §6 Roadmap | `okf/roadmap.md` (keep the checklist items and checked/unchecked state exactly as-is) | frozen (structure), checkboxes update in place |
   | §7 Risks & Mitigations | `okf/risks.md` | frozen |
   | §8 Current Status | `okf/status.md` | live |
   | §9 Open Questions & Blockers | `okf/open-questions.md` | live |
   | §10 Next Actions | `okf/next-actions.md` | live |
   | §11 Decision Log (D-000…D-029) | `okf/decisions/d-NNN-short-slug.md`, one file per decision, plus `okf/decisions/index.md` | append-only |
   | §12 Session Changelog (S-000…S-039) | `okf/changes/s-NNN-short-slug.md`, one file per session, plus `okf/log.md` (one line per session, newest first, linking to the changes file) and `okf/changes/index.md` | append-only |
   | §13 Key References | `okf/references/<slug>.md`, one file per reference (frontmatter `type: Reference`, `resource: <url or citation>`), plus `okf/references/index.md` | n/a (references are typically stable; treat as frozen) |
   | §14 LLM Update Protocol | fold into `.agents/skills/session-wrapup/SKILL.md` (new, adapted from the reference, but keep this project's own §11/§12 append-only mechanics and the canary/frozen-section rules from §0/§14) — not a content file | n/a |

3. **Migrate `docs/LESSONS_LEARNED.md`.** The reference bundle has no direct analog (it has no lessons file). Add `okf/lessons.md` (or, if it reads cleaner, `okf/lessons/<category>.md` per the file's existing five categories, plus an `okf/lessons/index.md`) with `mutability: live`. Preserve every pitfall losslessly — this file is high-value, don't summarize it away. Link it from `okf/index.md`.

4. **Automate the mechanical split, don't hand-transcribe.** §11 and §12 are ~70 entries total in a strict `` `D-NNN | date | ... | ...` `` / `` `S-NNN | date | vX.Y | ...` `` line format. Write a short throwaway Python script that parses `docs/PROJECT_TRACKER.md`, regex-splits each line, and writes one file per entry with the right frontmatter (mirror `append_okf.py`'s frontmatter shape) — far less error-prone than doing it by hand, and matches the reference bundle's own stated preference for scripts over manual edits to append-only content.

5. **Bring over the tooling, adapted, not copied verbatim.** Create `.agents/skills/edit-okf/` (with `scripts/append_okf.py`), `.agents/skills/session-start/`, and `.agents/skills/session-wrapup/` in this repo, adapted from the reference. Do **not** touch this project's existing `.agents/workflows/` (`research-cycle.md`, `verify.md`, `plan.md`, `execute.md`, `wrapup.md`, etc.) or existing `.agents/skills/` (`reviewer`, `critic`, `auditor`, `cross-validation`, `reproducible-run`, `documentation-publishing`, `python-simulation`, `research-analysis`, `cpp-engine`) — those are this project's own established pipeline and are out of scope.

6. **Update the pointers, not the content.** `AGENTS.md` currently says "You are the sole editor of `docs/PROJECT_TRACKER.md`; every edit follows the §14 update protocol" and references `docs/LESSONS_LEARNED.md`. Update these lines to point at `okf/` instead (respecting `AGENTS.md`'s own 12,000-character budget — check `wc -c AGENTS.md` after editing, and trim only the now-redundant §14-in-`AGENTS.md` prose if you need room, never the invariants in Sections I–III). Leave `CLAUDE.md`'s `@AGENTS.md` import line untouched.

7. **Retire the old files as redirect stubs, don't delete.** Once `okf/` is verified complete (step 8), replace the body of `docs/PROJECT_TRACKER.md` and `docs/LESSONS_LEARNED.md` with a short note: "This file's content moved to `okf/` on <date>. See `okf/index.md`. Kept as a historical pointer; do not add new content here." Do not delete the files outright — old links (e.g. from `docs/research/*` or `S-NNN` entries) may still reference them by path.

8. **Verify losslessness before finishing.** Diff every migrated fact against its source: every §11 decision, every §12 session line, every §13 reference, every LESSONS_LEARNED bullet must appear somewhere in `okf/`. Confirm every `index.md` (root and per-subdirectory) lists every file actually present in its directory — no orphaned files, no dangling links.

## Definition of Done

- [ ] `okf/` exists with all 14 tracker sections plus `LESSONS_LEARNED.md` represented, per the mapping above.
- [ ] Every `okf/decisions/d-NNN-*.md` (30 files, D-000–D-029) and `okf/changes/s-NNN-*.md` (40 files, S-000–S-039) exists, with `okf/log.md` carrying one line per session pointing at its changes file.
- [ ] Every `index.md` (root + `architecture/`, `model/`, `references/`, `decisions/`, `changes/`) is present, flat-list-only, and lists exactly what's in its directory.
- [ ] `.agents/skills/edit-okf/`, `session-start/`, `session-wrapup/` exist in this repo, adapted (not copy-pasted with stale paths) from the reference.
- [ ] `AGENTS.md` points at `okf/` instead of `docs/PROJECT_TRACKER.md`/`docs/LESSONS_LEARNED.md`, and is still under 12,000 characters.
- [ ] `docs/PROJECT_TRACKER.md` and `docs/LESSONS_LEARNED.md` are reduced to short redirect stubs, not deleted.
- [ ] `src/`, `cpp/`, `tests/`, `results/`, `viz/`, `section2-reformulation/` are untouched.
- [ ] A closing summary (in lieu of a PR, since this container has no git) lists every file added/moved/edited, so a human can review the working-tree diff directly.

## Watch-outs

- Don't let `okf/` `index.md` files grow prose — the spec is strict: headings + flat bullet links only, per the reference's own convention.
- Don't mark a migrated decision/session entry `frozen` — they're `append-only`; never edit their content once written, only transcribe it faithfully from the tracker.
- The tracker's §0 canary protocol (`Gary —` opening token) and §14 update protocol are *process* instructions for future sessions, not facts about the project — they belong in the new skills, not in an `okf/` content file.
