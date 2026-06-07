---
name: watchdog
description: Liveness monitor for parallel subagents. A recurring Scheduled Task reads each subagent's heartbeat and notifies (never auto-kills) when one goes stale. Treats an awaiting-approval pause as expected, so it never fights approval gates.
---

# Watchdog

Adapted from the teamwork-preview "crons to handle stuck or blocked processes" trick.
In the blog's fire-and-forget setting the watchdog auto-terminates and respawns stalled
subagents. Here, where subagents *legitimately* pause for Gary's approval, the default
action is **notify, not kill** — otherwise it would fight the approval gates (exactly the
"pytest timed out waiting for user permission" stall seen in the Week 2 run).

## Heartbeat protocol (each active subagent)
On every meaningful step, update `.agents/<role>/progress.md` with:

```markdown
last_heartbeat: <ISO-8601 timestamp>
status: RUNNING | BLOCKED:awaiting-approval | BLOCKED:waiting-input | DONE
current_step: <one line>
```

- A subagent that is waiting on Gary sets `status: BLOCKED:awaiting-approval` — this is
  **expected**, and the watchdog must not treat it as stuck.
- A subagent in a long compute step should still heartbeat at the start of the step so the
  watchdog can distinguish "working" from "hung".

## Checker logic (runs on the cron)
1. Read every `.agents/*/progress.md`.
2. For each, compute staleness = now − `last_heartbeat`.
3. Classify:
   - `status: BLOCKED:*` → **ignore** (this is intended; optionally remind Gary if a gate
     has been pending a very long time).
   - `status: RUNNING` and staleness > `STALE_THRESHOLD` (start with 20 min) → **flag as
     suspected-stuck**.
   - `status: DONE` → ignore.
4. For each suspected-stuck subagent, **notify** the Sentinel/Gary with its role, last
   `current_step`, and staleness. Do not auto-kill.

## Escalation (opt-in, narrow)
Auto-respawn is allowed **only** when ALL hold: the subagent is a read-only role
(e.g. `explorer`), it holds no pending approval, and it is not mid-worktree-edit. In every
other case — anything that writes, anything awaiting approval — notify and let Gary decide.
Never auto-kill a subagent that is mid-diff-application.

## Scheduled Task definition (create to activate — NOT created by this draft)
Create a Scheduled Task with roughly:

- **Schedule (cron):** `*/10 * * * *`  (every 10 minutes while a long run is active)
- **Prompt:**
  > Run the watchdog checker for the TwoCascade project. Read every
  > `.agents/*/progress.md`. For any file with `status: RUNNING` whose `last_heartbeat`
  > is more than 20 minutes old, notify me with the role, its `current_step`, and how
  > stale it is. Ignore files marked `BLOCKED:*` or `DONE`. Do not modify any project
  > files. Only auto-respawn a stalled subagent if it is read-only, holds no pending
  > approval, and is not mid-edit; otherwise just notify me.

Pause or delete the task when no long run is active so it isn't firing against an idle repo.

## Guardrails
- The watchdog **never edits project files** — it only reads `progress.md` and notifies.
- Notify-don't-kill is the default; auto-respawn is the narrow exception above.
- A pending approval gate is not a stall.
