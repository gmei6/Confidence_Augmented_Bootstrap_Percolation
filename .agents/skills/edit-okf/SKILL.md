---
name: edit-okf
description: Use when reading, creating, or editing files within the okf/ knowledge bundle (e.g., "update okf", "record a decision", session start/wrapup) to enforce OKF structural conventions - mutability, index syncing, decision/changelog numbering, and append-only enforcement.
---

# edit-okf Skill Instructions

Use this skill's logic when starting a session, ending a session, or anytime you are reading, creating, or editing files in the `okf/` directory, to enforce the bundle's structural and mutability conventions. The `okf/` bundle replaced `docs/PROJECT_TRACKER.md` and `docs/LESSONS_LEARNED.md` on 2026-07-04 (decision `okf/decisions/d-030-okf-migration.md`); those two files are now redirect stubs.

## Steps

1. **Observe Directory-Level Conventions**:
   - `okf/decisions/`: One file per decision, named `d-NNN-short-slug.md`. NNN continues the old tracker's `D-NNN` sequence (migration itself is d-030; the next new decision is d-031) — sequential, never reused, never renumbered. Frontmatter requires `type: Decision`, `mutability: append-only`, `timestamp` (ISO 8601), optional `tags`. Never edit a decision once written; if a decision is reversed or refined, write a new decision that supersedes it, and make both files say so explicitly. (Files d-000 through d-029 are verbatim migrations from the old tracker's one-line pipe format — `D-NNN | YYYY-MM-DD | Decision | Rationale | Affects §` — and any change to a frozen concept still requires a decision entry here, exactly as the tracker required one for any 🔒 section. New decisions use a short narrative body instead — state the decision, the rationale, and the affected concepts/§ labels.)
   - `okf/changes/`: One file per session/unit of work, named `s-NNN-short-slug.md` (sequential, continuing the old tracker's `S-NNN` sequence; migration is s-040). Frontmatter requires `type: Session Change`, `mutability: append-only`, `timestamp`, optional `tags`. It holds the full narrative of the session's changes. Note: s-011 through s-018 do not exist — they were already elided in the source tracker before migration.
   - `okf/log.md`: Reserved changelog. One line per session, newest first, each linking to its `changes/s-NNN-*.md` file. Never holds full narrative text itself.
   - `okf/references/`: One file per external source. Frontmatter requires `type: Reference`, `resource` (canonical URL or citation), optional `tags`.
   - `okf/cache/`: One file per cached source. Frontmatter requires `type: Cache`, `title`, `description`, optional `resource` (canonical URL or local path) and `tags`. Holds LLM-derived reference/study material (e.g. page maps, code cross-references) worth reusing rather than re-deriving each session — general-purpose, not limited to one source. `mutability: live` for both `cache/index.md` and every file within (see D-034) — unlike `decisions/`/`changes/`, cache entries are corrected in place, not superseded.

2. **Respect Mutability Frontmatter on Concept Files**:
   - `mutability: frozen` (identity, north-star, model/*, benchmark, architecture/*, roadmap, risks): Requires a decision file (`decisions/d-NNN-*.md`) explaining the change *before* editing. Then make the **minimal** edit, link the concept to the decision (and vice versa), and call the edit out to the user in your reply. Do not silently edit frozen files — **never** silently alter the North Star or the model definition; if a request pulls the work away from `okf/north-star.md` or contradicts a prior decision, surface the tension and ask before proceeding.
     - Exception: `okf/roadmap.md`'s structure is frozen but its checklist items are checked off in place as work completes (no decision file needed for a checkbox).
   - `mutability: live` (status, next-actions, open-questions, lessons, and most index files — `okf/index.md`, `architecture/index.md`, `model/index.md`, `references/index.md`, `cache/index.md`): Overwrite freely to reflect the current state — but truthfully. Don't mark something done that isn't; record blockers; a bundle full of optimistic fiction is worse than none.
   - `mutability: append-only` (`okf/log.md`, `changes/`, `decisions/`, **and their two index files** `decisions/index.md` / `changes/index.md`): Add new entries only. **CRITICAL**: You are strictly forbidden from using text editing tools to directly edit append-only files. You MUST use the provided Python script to append content: `python3 .agents/skills/edit-okf/scripts/append_okf.py <filepath> "<content>"` or pipe content into it (it also manages the read-only `chmod 444` lock on these files). Never edit prior entries. `decisions/index.md` and `changes/index.md` are the two exceptions to "all index files are live" (see D-032): their folders only ever gain entries, never rename or remove them, so their indexes only ever gain a bullet line too — when creating a new `d-NNN`/`s-NNN` file, append its index line via the same script, in the same step.

3. **Keep index.md Synchronized**:
   - Every `index.md` must follow the OKF spec exactly: one or more `#` section headings, each followed by a flat bullet list of `[Title](relative-path)` links. No prose outside the list.
   - Update the respective `index.md` whenever a file in its directory is added, renamed, or removed — except `decisions/index.md` and `changes/index.md`, which are `append-only` (see step 2): only ever append a new bullet, via `append_okf.py`, never rename or remove one.

4. **Maintain log.md and changes/ Pairing**:
   - When creating a `changes/s-NNN-*.md` file, simultaneously append its corresponding one-line entry to `okf/log.md` (new sessions go at the bottom; the file is append-only even though the migrated block reads newest-first).
   - Flag and fix any mismatch (a `changes/` file missing a `log.md` entry, or vice versa).

5. **Preserve the §N labels**: The migrated concept files keep their original tracker section labels (e.g. `# §4 — Analytical Benchmark`) in their headings, because `AGENTS.md`, `docs/research/*`, the `.agents/` workflows, and the decision entries all cross-reference them (`§5.4`, `§3.6`, …). Do not strip or renumber these labels.

6. **Follow the Session Workflow**:
   - **Start of session**: use the `session-start` skill (reads `okf/index.md`, the live files, and only task-relevant frozen files).
   - **End of session**: use the `session-wrapup` skill (overwrite live files; append one `changes/s-NNN-*.md` + its `log.md` line; append any `decisions/d-NNN-*.md` and link them to affected concepts; sync any `index.md` that gained or lost entries).
