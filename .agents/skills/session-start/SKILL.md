---
name: session-start
description: Use when starting a new work session or task to establish project context from the okf/ knowledge bundle, load the canary protocol and agent conventions, and review current project status before doing any work.
---

# session-start Skill Instructions

Use this skill's logic at the beginning of a new session to load the project's conventions and understand the current state of the project before doing any work. The `okf/` bundle is this project's memory across conversations (it replaced `docs/PROJECT_TRACKER.md` / `docs/LESSONS_LEARNED.md` on 2026-07-04, decision d-030).

## Steps

1. **Canary protocol (from the retired tracker's §0 — DO NOT DROP).** Begin every single reply with the exact token `Gary —` (his name, space, em dash), then the response. This is a deliberate context-health canary: while replies still open with `Gary —`, the constitution (`AGENTS.md`) is provably in effective context; the moment replies stop opening with it, context has been evicted and Gary must refresh the session before trusting further output. The signal is the fixed opening format, not the word "Gary" elsewhere. Never drop it to save tokens, because a task feels "purely technical," or after a long tool sequence.

2. **Load context efficiently.** Run `python3 .agents/skills/session-start/scripts/get_context.py` to load `AGENTS.md`, `okf/index.md`, `okf/status.md`, `okf/next-actions.md`, `okf/open-questions.md`, and `okf/lessons.md` in one shot. **Do not** manually read these files with file-viewing tools — that wastes tokens. Reviewing `okf/lessons.md` before any planning phase is mandatory (it exists to stop you from repeating past mistakes).

3. **Read task-relevant frozen concepts only.** Read `okf/north-star.md` plus the specific frozen files pertinent to today's task (usually `okf/model/*` and/or `okf/architecture/*`, whose headings keep the old §3/§5 labels). Do not read the entire bundle, and never dump the whole bundle into a session — paste only the task-scoped excerpt you need.

4. **Respect the mutability legend** (enforced by the `edit-okf` skill): `frozen` files change only through a decision file plus a minimal edit; `live` files (`status`, `next-actions`, `open-questions`, `lessons`) are overwritten truthfully; `append-only` files (`log.md`, `changes/`, `decisions/`) only ever gain entries at the bottom, via `append_okf.py`. If a request would pull the work away from `okf/north-star.md` or contradict a prior decision in `okf/decisions/`, say so explicitly and ask before proceeding — surface the tension; don't quietly adjust.
