---
name: session-wrapup
description: Use when completing a work session or task to document changes in the okf/ knowledge bundle - update live state, append the session change file and log line, record decisions, and run the honesty/sanity pass (adapted from the retired tracker's §14 update protocol).
---

# session-wrapup Skill Instructions

Use this skill's logic at the end of a session to ensure all work is documented properly in the `okf/` bundle. This folds in the retired tracker's §14 LLM Update Protocol; the `edit-okf` skill governs the file mechanics throughout.

## Steps

1. **Overwrite the live state truthfully.** Update `okf/status.md` (current phase, what got done, where new code lives, the latest validated result), `okf/open-questions.md` (refreshed open questions and real blockers), and `okf/next-actions.md` (the next few concrete steps, not a backlog dump). These files describe *now*, not history — overwrite stale content. Don't mark unfinished work done; record blockers; if you are unsure a result is correct, say so.

2. **Record new lessons.** Add any new codebase gotchas, performance constraints, or modeling discoveries to `okf/lessons.md` (live) — recording learnings at wrap-up is a standing invariant from `AGENTS.md`.

3. **Append the session change file.** Create `okf/changes/s-NNN-short-slug.md` (NNN = next sequential number; s-011–s-018 are a known gap, never backfill them) with a narrative summary of the session's work, frontmatter `type: Session Change`, `mutability: append-only`, `timestamp` (ISO 8601). **CRITICAL**: never use direct text-editing tools on append-only files — create/append via `python3 .agents/skills/edit-okf/scripts/append_okf.py <filepath> "<content>"` (or pipe content into it).

4. **Add the log line.** Append a single line to `okf/log.md` (same script) with the date, pointing to the new `changes/s-NNN-*.md` file.

5. **Record decisions.** For every decision reached this session — especially anything that changed a `frozen` concept file — append `okf/decisions/d-NNN-short-slug.md` (same script; state the decision, rationale, and affected concepts/§ labels), link it from the affected concept file(s), and call the frozen edit out to the user in your reply ("I changed okf/model/forks.md (§3.6) because of decision d-031"). A frozen file must never change without its decision file existing first.

6. **Guard the direction.** If the session pulled the work toward something at odds with `okf/north-star.md` or a prior decision, do **not** quietly fold it in — flag the tension and ask whether to record it as a deliberate pivot (new decision) or set it aside.

7. **Sync the indexes and tidy up.** Update any `index.md` that gained or lost entries (decisions/, changes/, references/, root). Check for stray scratch files or artifacts created during the session and remove or properly document them.

8. **Sanity pass before finishing:** Is the North Star intact? Do the live files reflect today? Is every decision and fork-resolution recorded in `okf/decisions/`? Is the change file appended and paired with its `log.md` line? Are frozen edits (if any) justified by a decision and flagged to the user? Record state, not source — note which module/script holds new code and what it does, but never paste source code into the bundle.
