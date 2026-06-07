---
name: execute
description: Execution workflow after a plan is approved: implement the changes, validate, and draft tracker updates. May spawn worker subagents by ownership (with a /watchdog); presents every diff for approval before writing. Called by /research-cycle Step 2.
---

# Execute

Implement a pre-approved plan. Honor all guardrails in GEMINI.md and AGENTS.md.

## Steps
1. **Context:** re-read the approved plan and the relevant tracker sections.
2. **Implement (may spawn subagents):** delegate code to the owning agents —
   `python-simulation` and/or `cpp-engine`. You MAY spawn these as parallel worker
   subagents when the plan has independent, non-overlapping units of work; give each its
   own worktree so they cannot corrupt one another or the validation baseline. Never
   modify `reference.py` (the oracle) or frozen sections as a side effect — STOP and ask.
   Never write `results/` directly — the runner owns output.
3. **Heartbeat + watchdog (long or parallel runs only):** every spawned subagent writes a
   heartbeat to `.agents/<role>/progress.md` per `/watchdog` (`last_heartbeat`, `status`,
   `current_step`); a subagent waiting on approval sets `status: BLOCKED:awaiting-approval`.
   When the run is long or runs workers in parallel, activate the `/watchdog` Scheduled
   Task so a stall is surfaced (notify, never auto-kill). Skip both for a trivial
   single-file change.
4. **Approve before writing:** present every diff in chat and get explicit permission
   before writing to disk. Prefer New Worktree Mode for changes to `src/` or `cpp/src/`.
   Spawning a subagent never bypasses this gate — each worker's diff is presented before
   it is written.
5. **Validate:** load the `cross-validation` skill if C++ changed; otherwise run pytest.
   (The full reviewer/critic/auditor gate is `/verify`, run next — don't duplicate it here.)
6. **Document:** have `documentation-publishing` draft the §11 decision and §12 changelog
   entries (drafts only; the PI applies them via §14).

## Long runs
If execution accumulates a large context (many subagent spawns or large diffs/logs),
invoke `/self-succession` at the budget threshold so context limits don't degrade the run.

## Report
Return an Execution Report mapping to the standard triplet:
[Files Changed] · [Validation Status] · [New Decisions], plus [Tracker text drafted].
