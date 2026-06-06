---
name: execute
description: Execution workflow. Use after a plan is approved to implement the changes, coordinate validation, and draft tracker updates. Delegates to the owning agents and presents diffs for approval before writing. Called by /research-cycle Step 2.
---

# Execute

Implement a pre-approved plan. Honor all guardrails in GEMINI.md and AGENTS.md.

## Steps
1. **Context:** re-read the approved plan and the relevant tracker sections.
2. **Implement:** delegate code to `python-simulation` and/or `cpp-engine` by ownership.
   Never modify `reference.py` (the oracle) or frozen sections as a side effect — STOP and
   ask. Never write `results/` directly — the runner owns output.
3. **Approve before writing:** present every diff in chat and get explicit permission
   before writing to disk. Prefer New Worktree Mode for changes to `src/` or `cpp/src/`.
4. **Validate:** load the `cross-validation` skill if C++ changed; otherwise run pytest.
5. **Document:** have `documentation-publishing` draft the §11 decision and §12 changelog
   entries (drafts only; the PI applies them via §14).

## Report
Return an Execution Report mapping to the standard triplet:
[Files Changed] · [Validation Status] · [New Decisions], plus [Tracker text drafted].
