@AGENTS.md

# CLAUDE.md — Claude Code Entry Point

> The `@AGENTS.md` line above imports the shared constitution (invariants, persona, guardrails, the **§0 canary protocol**, and every `§N` reference into `docs/PROJECT_TRACKER.md`). Claude Code does **not** read `AGENTS.md` natively, so that import line is what loads it — keep it as the first line of this file. **Put shared rules in `AGENTS.md`, not here.** This file holds only Claude-Code-specific mechanisms.

---

## Baseline isolation — the worktree mechanism

Implement the `AGENTS.md` baseline-isolation guardrail by developing any change to `src/` or `cpp/src/` in a dedicated git worktree — e.g. `git worktree add ../tc-work <branch>` — keeping the known-good baseline on the main checkout. Documentation, config, and clearly-scoped single-file fixes may be edited in place.

---

## Permissions — enforce the `AGENTS.md` policy via settings

Mirror the `AGENTS.md` permission policy in `.claude/settings.json` permission rules:

- **Ask before:** `git commit`, `git push`, any file deletion.
- **Deny:** `git push --force`, `rm -rf`, any direct write to `results/`.
