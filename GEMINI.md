# GEMINI.md — Antigravity-Specific Overrides

**Project: TwoCascade** (bootstrap percolation / confidence-threshold cascade simulation)

> General project rules, tech stack, and code standards live in `AGENTS.md`. This file contains only Antigravity-specific behavioral overrides. When a rule in this file conflicts with `AGENTS.md`, this file wins.

---

## Agent Mode

Prefer **New Worktree Mode** for any change to `src/` or `cpp/src/`.

* The Python reference implementation and C++ engine must stay in a known-good state at all times.
* Worktree isolation ensures experimental changes don't corrupt the validation baseline.
* Use **Local Mode** only for documentation, config, or clearly scoped single-file fixes that carry no risk of breaking cross-validation.

---

## Guardrails

* **Propose, Don't Write:** You must never write code or file changes to disk using writing tools (such as `write_to_file`, `replace_file_content`, or `multi_replace_file_content`) without first presenting the proposed diff or code block in the chat and asking the user for permission. Only apply the edits after the user has explicitly approved them.
* **Oracle Protection:** `src/twocascade/reference.py` is the cross-validation oracle. It must never be modified as a side effect of other work. Any session that touches it requires an explicit, standalone instruction. If changes to `model.py`, `runner.py`, or the C++ engine imply the reference should be updated, stop and ask rather than propagating the change automatically.
* **Results Integrity:** Never write to `results/raw/` or `results/figures/` directly. The runner script is responsible for all output, and it stamps each file with seed, parameter tuple, and git commit hash. If asked to write results directly, flag the provenance concern and redirect to the runner.
* **Research Document Edits:** Before editing any file in `docs/research/`, state which research question (Q#) or falsifiable conjecture (F#) the change affects and summarize what is being revised. These are auditable research artifacts, not living notes.
* **Test Semantics:** Before modifying a test in `tests/`, distinguish explicitly between two cases: (a) the test was wrong and is being corrected, or (b) a code change broke a previously valid test. These require different responses and should never be conflated.

---

## Artifact Conventions

Adapt the standard Plan → Execute → Verify loop to the research context.

* **`task.md`**: Include the simulation parameters and theoretical invariants under test, not just code tasks. A task that changes threshold behavior should name the relevant conjecture.
* **`implementation_plan.md`**: For any change to the C++ engine, include a section stating whether the Python reference needs a parallel update and why. For any change to the Python layer, state whether C++ parity is in scope for this session. Never leave this implicit.
* **`walkthrough.md`**: The proof of work for simulation-relevant changes must include the cross-validation result: Python reference vs C++ engine run on an identical seed and parameter set, with outputs confirmed to agree.

---

## Permissions (Configure in IDE, not here)

Set the following in **Agent Manager → Additional Options → Customizations → Permissions**. Do not manage them in this file.

| Action Level | Guarded Actions |
| --- | --- |
| **Always Ask** | `git commit`, `git push`, any file deletion |
| **Always Deny** | `git push --force`, `rm -rf`, direct writes to `results/` |

---

## Workflow

* **Primary entry point:** `/research-cycle`
* **Definition at:** `.agents/workflows/research-cycle.md`
* **Verification:** Verification is the `/verify` workflow — `reviewer` → `critic` → `auditor`, each spawned blind. Pass the `walkthrough.md` artifact from the preceding implementation session as input context. The `auditor` returns a binary AUDIT PASS/FAIL and is the mandatory gate before any result is marked done.