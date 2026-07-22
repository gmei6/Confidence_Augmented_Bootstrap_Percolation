---
type: Session Change
title: "S-060 — Advisor meeting 2026-07-22: poster directive, two-comparison framework, publication route resolved"
mutability: append-only
timestamp: 2026-07-22
tags: [advisor, meeting, poster, scope]
---

# S-060 — Advisor meeting 2026-07-22 (Prof. Dhara)

Live meeting notes, consolidated same-day. No code or results changes this session.
Cleaned verbatim notes: `okf/meeting-notes/2026-07-22-dhara.md`.

## Advisor's framing of the model
- He frames the model as a **Markov chain studied through its stopping time**: run the chain,
  stop when a condition hits (e.g. number of failed nodes crossing a threshold, or any
  stopping condition).
- Core difficulty in this area: stopping times are often **exponential in network size**,
  which makes simulation at realistic scale (10⁶–10⁷ nodes) hard.
- **Healing deferral validated**: he agreed it made sense not to implement recovery/healing
  (consistent with D-031; the exponential-stopping-time / metastability concern is a further
  argument for keeping the process monotone).

## Geometry remarks
- Uniform-at-random points → few points near the boundary (boundary-effect observation;
  our torus already avoids hard boundaries — not further clarified in the meeting).
- A viable regime: **hard RGG topology with a tiny number of affected nodes**.
- **GIRG endorsed**: "a flexible model, the most general model" — implicitly answers the
  GIRG-promotion question (yes, worth the engineering).

## Headline directive: the next deliverable is a POSTER
He said there is already enough material for a good poster. The poster is built on **two
controlled comparisons, kept separate**, each at matched n and matched average degree:

1. **Effect of degree heterogeneity** (no geometry): **Erdős–Rényi vs configuration model**,
   identical mean degree and n; plot number infected / P(systemic) across the two.
   (ER currently has zero runs — it is the untested cell of the 2×2.)
2. **Effect of geometry** (heterogeneity held fixed): **configuration model vs GIRG**, with
   GIRG parameters set so the **degree distribution matches** the configuration model — one
   has geometry, the other does not. Also ER vs GIRG at matched average degree.
- Nice-to-add: **hard RGG in increasing dimension D** — does the result change with D?
- Narrative: **ER is the baseline, justified by citing Janson's paper** — "here is the
  framework, here is what I build on it, here is my conceptual question." Goal statement:
  understand the effect of degree heterogeneity and geometry, with fear/panic driven by
  localized events.

## ISyE requirement: a recommendation component
The project needs a **policy/intervention angle**: how to keep checks and balances to stop
the process from spreading — "with this new model, what can I say?" New axis, previously
untouched.

## Publication route (the one open question) — RESOLVED
- **Yes** to pushing to the frontier (theoretical or empirical) after ~6 months of work;
  he will help.
- Empirical path made concrete: **SNAP dataset** — code exists, download one dataset, apply
  the framework, check whether real-network behavior matches the inhomogeneous
  with/without-geometry expectations. "Might not hurt to show I'm already thinking about
  real-world data."

## Logistics
- **Next meeting: the poster**, plus a brief chat about real-world data / conclusions.

Decision recorded: D-038. Live files updated: status, open-questions, next-actions.
New folder created: `okf/meeting-notes/` (cleaned meeting notes, indexed).
