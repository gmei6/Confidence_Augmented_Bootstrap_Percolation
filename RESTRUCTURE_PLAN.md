# Repo Restructure Plan (2026-07-07)

**Status: PLANNING — nothing in this document has been executed.** This is the
consolidated output of a planning conversation between Gary and Claude Code. Execute
in the phase order below; each phase depends on the ones before it. Re-verify counts
(`grep`/`git ls-files`) before executing, since the repo will have moved on since this
was written.

## Why

Two goals: (1) general repo hygiene — stray files, stale docs, dead duplicates; (2)
give Claude Code and Antigravity the **same experience** — same constitution, same
skills, same slash commands — instead of two tools reading two different files with
drifting content.

---

## Decision log (what was actually decided, and why)

| # | Item | Decision | Rationale |
|---|---|---|---|
| 1 | `pyproject.toml` | **Keep** | Makes `pip install -e .` work (D-013); deleting would force `sys.path` hacks everywhere. |
| 2 | `GEMINI.md` | **Retire** | Gary confirmed Antigravity now reads `AGENTS.md` directly. Useful tool-specific content gets folded into `AGENTS.md` first (see Phase 1). |
| 3 | `CLAUDE.md` | **Symlink → `AGENTS.md`** | Its two unique bits (worktree command, `.claude/settings.json` pointer) get folded into `AGENTS.md`'s new "Tool-specific mechanisms" section first, so nothing is silently lost. |
| 4 | `.agents/skills/` (12 skills) | **Keep all, no pruning** | `reviewer`/`critic`/`auditor` are the mandatory blind verify gate (AGENTS.md §IV); `cross-validation`/`cpp-engine`/`python-simulation`/`research-analysis`/`reproducible-run`/`documentation-publishing` are live domain skills, not legacy. |
| 5 | `no-mistakes` (external tool) | **No repo change** | Already usable via `/no-mistakes`; it's a generic push/CI gate, explicitly *not* a replacement for the project's own review architecture — complements it. |
| 6 | `run_girg_sim.py` | **Move → `scripts/`** | Matches where every other task driver lives. |
| 7 | `docs/queue/task_{E,F,G,H,N,O,P}.md` | **Move → `old-tasks/`** | They're done; the queue's own convention already does this for I/J/K/L/M. |
| 8 | `.DS_Store` (root **and** `docs/`) | **Untrack both** | Already gitignored going forward; only the already-committed copies need `git rm --cached`. |
| 9 | `HOWTOUSE.md` | **Delete** | References paths (`docs/antigravity_queue/`, `CABP_copy_for_antigravity`) that don't match this repo — looks copied from the sandbox-copy environment. |
| 10 | `docs/PROJECT_TRACKER.md`, `docs/LESSONS_LEARNED.md` | **Delete outright** (not migrated) | Dead since the S-040 `okf/` migration. **Only safe after Phase 1** — see below, they're currently load-bearing redirect stubs. |
| 11 | `docs/{research,queue,benchmarks,understanding_janson,potential_ideas,souvik_dhara_markdown}/` | **Move → `okf/*`** (flattened, siblings of `decisions/`, `changes/`, `model/`) | Consolidate all *knowledge* into one scan-first folder (Gary's stated goal: teach agents to check `okf/` before acting). |
| 12 | `results/` | **Move → `okf/results/`** | Same consolidation goal. Data, not prose — stays unformatted (no okf frontmatter), just relocated. |
| 13 | `section2-reformulation/` | **Move → `viz/section2-reformulation/`** | Reclassified: it's a deployed static site, not knowledge — belongs with `viz/`, not `okf/`. |
| 14 | `viz/` root content (the interactive tutorial) | **Move → `viz/tutorial/`** | Makes room for multiple sites under one `viz/` folder. |
| 15 | `viz/` root | **New landing page** | Small new `index.html` linking to `viz/tutorial/` and `viz/section2-reformulation/` so the root URL isn't dead. |
| 16 | `.claude/skills` | **New symlink → `.agents/skills`** | `.agents/skills/*/SKILL.md` already use Claude Code's exact `name`/`description` frontmatter — free drop-in. |
| 17 | `.claude/commands` | **New symlink → `.agents/workflows`** | Gives Claude Code the same `/research-cycle`, `/plan`, `/execute`, `/verify`, `/wrapup`, etc. Antigravity already has. **Only safe after the Phase 1 workflow-file fix below.** |

---

## The prerequisite bug (found while scoping #17)

`docs/PROJECT_TRACKER.md` and `docs/LESSONS_LEARNED.md` are not dead files — they are
**deliberate one-paragraph redirect stubs**, and their own text says why: *"Kept as a
historical pointer because... `.agents/` workflows... reference this path; do not add
new content here."* The S-040 migration author knew this cleanup was owed and left the
stub as a safety net instead of doing it.

**11 of the 12 files in `.agents/workflows/` still read `docs/PROJECT_TRACKER.md` /
`docs/LESSONS_LEARNED.md` directly and mention `GEMINI.md` by name:**
`advisor-prep.md`, `execute.md`, `harden.md`, `improve-agents.md`, `new-experiment.md`,
`plan.md`, `research-cycle.md`, `self-succession.md`, `session-start.md`, `verify.md`,
`wrapup.md`. (`watchdog.md` is already clean.)

These must be fixed **before** deleting the two doc stubs (item 10) and **before**
symlinking `.claude/commands` (item 17) — otherwise both tools' primary entry points
silently break on a missing file. Fix pattern per file:

- `docs/PROJECT_TRACKER.md` §N references → the specific `okf/*` file per the stub's own
  map: §2→`north-star.md`, §3→`model/`, §5→`architecture/`, §8→`status.md`,
  §9→`open-questions.md`, §10→`next-actions.md`, §11→`decisions/`, §12→`changes/`.
- `docs/LESSONS_LEARNED.md` → `okf/lessons.md`.
- "Honor GEMINI.md and AGENTS.md" / "GEMINI.md and AGENTS.md" → just `AGENTS.md`.

---

## AGENTS.md changes (Phase 1)

Add a new subsection in §III (replacing the current "see GEMINI.md/CLAUDE.md"
pointers in the baseline-isolation bullet and the Permission-policy heading):

```markdown
### Tool-specific mechanisms

- **Claude Code** — baseline isolation via `git worktree add ../tc-work <branch>` for
  any change to `src/` or `cpp/src/`. Permissions enforced via `.claude/settings.json`.
- **Antigravity** — baseline isolation via **New Worktree Mode** for `src/`/`cpp/src/`
  changes, **Local Mode** otherwise. Permissions configured in **Agent Manager →
  Additional Options → Customizations → Permissions**, not in a file. "Propose, don't
  write" binds specifically to `write_to_file`, `replace_file_content`, and
  `multi_replace_file_content`. Primary workflow entry: `/research-cycle`
  (`.agents/workflows/research-cycle.md`); `/verify` runs the reviewer→critic→auditor
  gate (§IV).
```

Rewrite the two architecture-description bullets near the top:

```markdown
- **Antigravity** loads this file natively.
- **Claude Code** does **not** read `AGENTS.md` natively; `CLAUDE.md` is a symlink to
  this file so Claude Code picks it up automatically.
```

Also update §IV's "(Tool-specific invocation — e.g. the Antigravity `/verify` workflow
— is defined in `GEMINI.md`.)" to point at the new Tool-specific mechanisms section
instead. Update the Permission-policy section's "any direct write to `results/`" to
"any direct write to `okf/results/`" once Phase 3 lands (not before — sequencing
matters, don't rename the path in AGENTS.md before the directory actually moves).

Length check: AGENTS.md is 7,803 characters today; the addition above is roughly
1,000–1,200 characters. Total lands around 9,000 — comfortably under Antigravity's
12,000-character silent-truncation limit.

---

## Execution phases

**Phase 1 — Tool unification** (do this first; everything else depends on it)
1. Rewrite `AGENTS.md` per the section above.
2. Fix the 11 stale `.agents/workflows/*.md` files (see prerequisite-bug section).
3. Delete `GEMINI.md`.
4. Replace `CLAUDE.md` with a symlink to `AGENTS.md`.
5. Create `.claude/skills` → symlink → `.agents/skills`.
6. Create `.claude/commands` → symlink → `.agents/workflows`.
7. Delete `docs/PROJECT_TRACKER.md`, `docs/LESSONS_LEARNED.md` (now safe).

**Phase 2 — Small cleanups** (independent, low risk, can happen anytime)
1. `git mv run_girg_sim.py scripts/run_girg_sim.py`.
2. `git rm --cached .DS_Store docs/.DS_Store`.
3. Delete `HOWTOUSE.md`.
4. `git mv` the seven finished `docs/queue/task_{E,F,G,H,N,O,P}.md` → `docs/queue/old-tasks/`
   (or fold this into the Phase 3 `docs/queue → okf/queue` move — do it in whichever order
   is convenient, just before or as part of that move).

**Phase 3 — Big consolidation** (highest file-count, highest risk — do in an isolated
branch/worktree even though it doesn't touch `src/`/`cpp/src/`, purely for the ability
to cleanly bail)
1. `git mv` each of `docs/research`, `docs/queue`, `docs/benchmarks`,
   `docs/understanding_janson`, `docs/potential_ideas`, `docs/souvik_dhara_markdown`
   into `okf/` (flattened, no `docs/` stutter).
2. `git mv results okf/results` for tracked files; plain `mv` for the untracked raw
   JSON currently on disk (verify current tracked/untracked split with
   `git ls-files results/` before moving — it was 21 tracked files as of 2026-07-07).
3. `git mv` today's `viz/` root content (`index.html`, `app.js`, `cascade.js`,
   `walkthrough.js`, `tutorial.js`, `style.css`, `vendor/`, `README.md`) into
   `viz/tutorial/`.
4. `git mv section2-reformulation viz/section2-reformulation`.
5. Write a new `viz/index.html` landing page linking to `viz/tutorial/` and
   `viz/section2-reformulation/`.
6. Rewrite `.github/workflows/pages.yml`:
   - `on.push.paths`: `viz/**` (now covers both sites), `okf/results/figures/**`,
     `.github/workflows/pages.yml`.
   - Build step: copy each `viz/` subfolder (plus the new root landing page) instead of
     flattening `viz/.` to site root; repoint the figures copy from `results/figures/`
     to `okf/results/figures/` (site-served path can stay `_site/results/figures/`).
7. Rewrite `.gitignore`'s `results/*` patterns to `okf/results/*`.
8. Rewrite path-string references across the repo (re-`grep` to get current counts —
   they were roughly: 139 files referencing `results/`, 16 referencing
   `docs/research|queue|benchmarks|understanding_janson`, 12 referencing
   `section2-reformulation`, as of 2026-07-07). This includes all `configs/*.json`
   `output.raw_filepath` fields, all scripts with hardcoded `results/...` paths, and
   every doc that links to the moved paths.
9. `okf/architecture/repo-layout.md` (§5.3) is `mutability: frozen` — do not edit it
   directly. Write a new `okf/decisions/d-0NN-*.md` entry describing the layout change
   first (per the `edit-okf` skill protocol), then make the minimal corresponding edit
   to `repo-layout.md`.
10. Update `AGENTS.md`'s permission-policy text: "any direct write to `results/`" →
    "any direct write to `okf/results/`".

**Phase 4 — Verification** (mandatory before merging/committing)
1. Run the full `pytest` suite.
2. Run one existing sweep end-to-end (small `n`, few trials) to confirm config
   `output.raw_filepath` and script-relative paths still resolve post-move.
3. Validate `.github/workflows/pages.yml`'s new paths (YAML lint at minimum; ideally a
   `workflow_dispatch` test run after pushing, since GH Actions can't be fully
   simulated locally).
4. `git status` sanity check — confirm `.gitignore` still excludes the right things and
   nothing unexpected got tracked or left behind.
5. Present a full diff summary to Gary for review before merging into `antigravity` or
   pushing — per AGENTS.md's "propose, don't write" and "ask before git commit/push"
   rules, this applies to the restructure exactly like any other change.

---

## Open items not yet decided

None outstanding as of 2026-07-07 — every item above has an explicit decision. If
re-scoping this plan in a future session, re-verify the file counts in Phase 3 step 8
first, since new commits between now and execution will have changed them.
