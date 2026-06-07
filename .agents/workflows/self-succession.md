---
name: self-succession
description: Context-preservation protocol for long runs. When the orchestrator's context fills, it dumps full state to a handoff file and spawns an identical successor that resumes from it. Carries guardrail state forward; never auto-approves.
---

# Self-Succession

Adapted from the Antigravity teamwork-preview "self-succession" trick, constrained for a
human-in-the-loop research repo. Honor all guardrails in GEMINI.md and AGENTS.md. This
protocol writes only to `.agents/<role>/handoff.md` scratch files — never to `src/`,
`cpp/`, `results/`, the tracker, or `reference.py`.

## When to succeed
The orchestrator tracks a **succession budget** and triggers when either crosses its
threshold (tune to taste):
- cumulative subagent spawns this session ≥ `N` (start with N≈12), or
- context window estimated near its limit (e.g. a long execute/harden run with large
  diffs and logs accumulated).

Succeed at a **clean boundary** — between milestones or after an approval gate resolves —
never mid-diff-application or while a write is pending approval.

## Handoff schema — `.agents/<role>/handoff.md`
Write the complete state needed to resume cold. Mirror the existing BRIEFING style:

```markdown
# HANDOFF — <ISO-8601 timestamp>

## Mission
<one line: the active goal>

## North Star check
<§2 North Star restated; confirm intact, or flag the tension that must be resolved>

## Milestone & progress
- Current milestone: <name>
- Done so far: <bullets>
- In flight: <what was mid-step at handoff>

## Guardrail state (carry forward — do NOT reset)
- Pending approval gates: <every diff/action awaiting Gary's approval — STILL PENDING>
- Worktree state: <branch/worktree, clean or with un-merged isolated edits>
- Anything touching reference.py / frozen §sections / results: <should be NONE; if not, STOP>

## Decisions made (draft §11)
- D-NNN (draft): <decision + rationale>

## Open threads / blockers
- <questions for Gary, stuck checks, deferred items>

## Next concrete actions
1. <first thing the successor should do>
2. ...

## Artifact index
- <paths to walkthrough.md, progress.md, plan.md, configs, raw outputs>
```

## Succession steps
1. **Quiesce.** Finish or cleanly pause the current step. Do not start a new write.
2. **Dump.** Write the handoff file per the schema above. Be exhaustive about *pending
   approvals* and *worktree state* — these are what a cold successor most easily loses.
3. **Stop background tasks.** Kill the parent's own background/long-running tasks so they
   don't outlive it (the watchdog cron, which is project-level, keeps running).
4. **Spawn successor.** Start a new orchestrator subagent with **identical** goals,
   permissions, and briefing. Its first action is Step 0 of `/research-cycle` (read
   tracker + LESSONS_LEARNED) followed by reading this handoff file.
5. **Terminate parent.** The parent exits once the successor confirms it has loaded the
   handoff.

## Guardrails (non-negotiable)
- **No auto-approval across succession.** Anything that was awaiting Gary's approval
  before the handoff is still awaiting it after. The successor must re-present, not assume.
- **Propose-don't-write survives.** The successor inherits the same write restrictions;
  succession is not a loophole to apply unreviewed edits.
- Handoff files are scratch (`.agents/`), not auditable research artifacts — but they must
  be truthful: never record unfinished work as done.
