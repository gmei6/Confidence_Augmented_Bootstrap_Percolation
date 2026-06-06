---
name: session-start
description: Run at the start of every new conversation to load project memory. Reads the tracker and lessons, restates the North Star, and surfaces current status, open questions, and next actions before any work begins.
---

# Session Start

The tracker is the project's memory across conversations (§0). Load it before doing anything.

## Steps
1. Read `docs/PROJECT_TRACKER.md` in this order: §2 North Star → §8 Current Status →
   §9 Open Questions/Blockers → §10 Next Actions. Then read `docs/LESSONS_LEARNED.md`.
2. Read the 🔒 sections relevant to today's likely task (usually §3 Model and/or §5 Coding
   Standards) only as needed.
3. Report a short orientation:
   - The North Star in one sentence (confirm it is intact).
   - Current phase and the latest validated result.
   - Open questions / blockers.
   - The next 1–3 concrete actions from §10.
4. Ask what the user wants to tackle, and flag immediately if their intent conflicts with
   the North Star or a prior decision (§11) — surface the tension before proceeding.

Read-and-orient only. This workflow edits nothing.
