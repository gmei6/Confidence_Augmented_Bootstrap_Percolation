# Task M — Scoping doc: optional recovery/healing phase (Q7)

**One-line task.** Produce a design document for the lower-priority Q7 extension (D-028): an SIR-style optional recovery/healing phase, as a model variant on top of the current permanent-activation (SI-style) dynamics.

**Touches:** new `docs/research/q7_recovery_phase_scoping.md`. Read-only against everything else.

## Environment note (read first)

No git access in this container, on purpose — do not attempt `git commit`/`push`/`branch`/`worktree`. This task only writes one new file under `docs/research/`; edit in place, no isolation needed. Design document only — do not modify `src/`, `cpp/`, or `results/`.

## Why this is low-human-input

Same shape as Tasks J/K/L: a design exercise ending in a spec, no simulation, no code. This is explicitly marked **lower-priority** in §9 (Q7) — treat this task as backup/optional work, not urgent.

## Context to read first

- `docs/PROJECT_TRACKER.md` §3.4 (Dynamics & stopping rule — the current permanent/absorbing failure assumption this extension would relax), §9 Q7, D-028 in §11.
- `docs/LESSONS_LEARNED.md` in full.
- If `okf/` exists by the time this task runs (Task I may have completed), read the equivalent `okf/model/` files instead of the tracker sections above.

## Plan

1. **State precisely what changes.** Currently: "failure is absorbing (a failed bank stays failed)" (§3.1) and the process halts at the first quiet round (§3.4). Define a recovery mechanism: e.g. a failed bank recovers with per-round probability $\rho$ (or after a fixed recovery time $\tau$), becoming solvent again and re-eligible for both channels (solvency §3.2, fear §3.3).
2. **Work out what breaks.** The absorbing-state halting rule (§3.4) no longer applies as-is once recovery exists — the process could oscillate indefinitely. Propose a new, well-defined stopping rule (e.g. fixed horizon $T$, or "stops when the failed fraction has been below some $\epsilon$ for $K$ consecutive rounds"). Also check: does $R_{\text{fear}} \approx \mu < 1$ (§3.3's central subcriticality fact) still hold with recovery, or does a recovering population change the effective reproduction number? Work this out explicitly, don't assume it's unaffected.
3. **Connect to the North Star (§2).** State plainly whether this variant changes the paper's central claim (the systemic-event phase diagram) or is purely a robustness/extension check on top of it — this determines whether it's an MVP-adjacent result or a true stretch item, consistent with how §6 already brackets it as low-priority stretch.
4. **Formulate a falsifiable conjecture** for what recovery does to the phase diagram (e.g. "recovery raises the effective critical seed $a_c$ and can eliminate the systemic phase entirely once $\rho$ exceeds some threshold tied to $\mu$").
5. **Write the implementation plan** (per `AGENTS.md` Section IV's `implementation_plan.md` convention): what changes in `src/twocascade/model.py`/`reference.py` (note: `reference.py` is the oracle — per `AGENTS.md` Section III, any implied change to it requires a standalone, explicitly-approved instruction; flag this rather than assume it in scope) and whether the C++ engine needs a parallel change.

## Definition of Done

- [ ] `docs/research/q7_recovery_phase_scoping.md` exists, self-contained.
- [ ] The new stopping rule is fully specified (the current absorbing-state halting rule does not transfer as-is — this must be addressed, not glossed over).
- [ ] Whether/how $R_{\text{fear}} < 1$ subcriticality is affected by recovery is explicitly worked out.
- [ ] The doc states plainly whether this is MVP-adjacent or pure stretch, and flags that any implied `reference.py` change needs separate, explicit approval (oracle-protection rule).
- [ ] No file outside `docs/research/` is modified.

## Watch-outs

- Don't silently assume the halting rule "just works" with recovery — an oscillating or non-halting process is a real risk worth naming, per this project's own honesty norms ("Be honest in the live state," tracker §0 rule 3).
- `src/twocascade/reference.py` is the oracle (`AGENTS.md` Section III) — this task should design around it, not propose editing it as a side effect.
