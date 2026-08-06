---
type: Concept
title: "Poster presentation script"
description: "The spoken walk for the SURS poster — baseline-first arc per D-046; matches the S-066 final poster layout."
mutability: live
---

# CABP Poster Presentation Script (S-066 final, 2026-08-06, rev. 2)

Matches the submitted poster (Gary's Overleaf revision, reconciled): model
schematic lives on the **demo site's landing screen** (not the poster); the
left column runs Existing Work → The contribution → How is fear defined? →
What We Look For; the top-right panel is the **probability figure** ("What
happens when only 2 nodes fail?", μ̄ 0→1.0 including the new ext2 arms);
panel titles carry the framing (no printed question lines); How To
Intervene carries three printed AUDIT-PASS anchors; QR caption reads "Scan
to interact with live graphs." Full run ~5.5 min; with the 15-second hook
compression, ~4 min.

## 1. The Hook (The Problem)

Let me paint a hypothetical for you. You're the happy owner of a small
regional bank on September 14, 2008. By small, I mean *small* — no
connections to any larger out-of-state banks. Everyone else hopped onto the
trend of subprime mortgage-backed securities, but you kept things simple and
avoided the hype.

The very next day, Lehman Brothers collapses. Initially, you aren't too
worried. Your bank has no financial connections to them. The banks that lent
them money are in deep trouble — but you didn't, so you don't think twice.
You operated safety-first.

But as more banks fail, your depositors get progressively more anxious. *If
Lehman Brothers could collapse, who's next?* That anxiety builds, and before
you know it, there's a bank run. Almost all your customers demand their
money at exactly the same time. Despite your prudent lending, your bank
fails anyway.

*(15-second compression, for mid-conversation walk-ups: "Imagine a prudent
small bank in September 2008 — zero Lehman exposure, fails anyway, because
its depositors panicked. Structure didn't kill it; fear did. That's the gap
in the standard model.")*

## 2. The Baseline (What Exists)

**[Point at "Existing Work", left column — the three graph families]**

How would you model this? Classically, network contagion is modeled purely
through structural connections: a node fails only once $r$ or more of its
neighbors have already failed. This is **bootstrap percolation**, and the
canonical sharp analysis is Janson et al.'s, on the Erdős–Rényi graph —
every pair of nodes connected with probability $p$. Their work answered the
big questions for that baseline:

1. What initial seed size ignites a full cascade?
2. How sharp is the transition?
3. How large is the final cascade?
4. How long does it take?

It's *the* baseline because it's exactly solvable. But notice what it can't
do: in that model, my prudent little bank **cannot fail**. It has no failed
neighbors. The model has no channel for panic.

## 3. Our Model (What I Did)

**[Point at the two numbered rules under "The contribution" and the fear
definitions under "How is fear defined?"; the visual version is the first
thing the demo site shows — invite a scan if the listener wants the
picture]**

So I add one. Every node keeps the structural route — at least $r = 2$
failed neighbors and it fails next round. That's the baseline mechanism,
unchanged.

The new route is **fear**. I give each node a fear susceptibility $f_i$ —
how prone it is to panic, drawn once at the start. Then there's a global
fear signal $g_t$: the share of the network that has failed *recently* —
the last few rounds, not all of history. Each round, every healthy node
fails **with probability $f_i \times g_t$** — a fresh coin flip every
round. The more the network just burned, and the more anxious the node, the
likelier it panics — even with *zero* failed neighbors. That's my small
bank from 2008: structurally safe, killed through the fear channel.

## 4. The Goal (Why These Comparisons)

Real networks aren't Erdős–Rényi. They have **hubs** — a few nodes holding
most of the edges — and **locality** — you're more connected to who's near
you. So in addition to the solved baseline, we need to model the effect of
fear on networks *with* heterogeneity and geometry. That's this project.

Everything on this poster holds $n$ and average degree fixed — all three
families matched to the same mean degree — so each comparison isolates
exactly one thing: heterogeneity, geometry, and fear.

## 5. The Results

**[Point at the main center graph]**

Here's the headline, and it surprised us. At matched mean degree, moving
from the homogeneous graph to a hub graph moves the ignition threshold by a
factor of **thirty** — Erdős–Rényi needs ~314 seed failures to tip, the hub
networks need ~10. Adding geometry on top of hubs moves it about **twelve
percent** — 11.4 versus 10.2. **Hubs, not distance, set the threshold.**
And within the hub families, fear's effect is nearly identical with or
without geometry — the curves interleave. These are verified numbers — the
full analysis pipeline cleared an independent audit.

*(If a technical viewer asks about implementation — the printed disclosure
was cut for audience legibility, D-047, so this is YOURS to say: "ER runs
on our validated C++ engine, the power-law model on the Python reference
implementation, and GIRG on both — cross-engine agreement is verified, so
the comparison isn't an engine artifact.")*

**[Point at top right: "What happens when only 2 nodes fail?"]**

This panel fixes a *tiny* seed — two failures — and turns the fear dial
from zero all the way to one. Watch the three curves. The hub networks
respond to fear immediately and smoothly — a few percent at low fear,
climbing to about half of all trials cascading at maximal fear. But look at
the Erdős–Rényi line along the bottom: **flat at exactly zero all the way
through μ̄ = 0.7.** Five hundred trials per point, not one cascade. It
doesn't ignite at all until fear reaches 0.8 — and even then in only about
2% of trials. **Fear amplifies cascades the structure makes possible. It
essentially cannot start them alone** — on the homogeneous network it takes
near-certain panic to light two failures into anything.

*(Spoken color, if asked "how much more likely":)* on the hub networks
that's roughly a 3× multiplier at moderate fear, 7-8× at high fear; on
matched Erdős–Rényi at a comparable starting risk it's at least 26× — at
least, because every trial cascaded and we hit the measurement ceiling.

*(Pivot line:)* That's the probability view at a fixed shock. Now flip the
question — fix the target instead, and ask how small a spark suffices.

**[Point at "Fear and Structure"]**

At moderate fear, fear cuts Erdős–Rényi's tipping point by **65%** — but
cuts the hub networks' by only **~35%**. Hubs blunt fear's effect.
Geometry, again, doesn't change that. Notice this is the *same verdict* the
probability panel reached, from an independent measurement — two
projections of one phenomenon, agreeing. *(Spoken-only, off the print:)*
fear also makes the transition *sharpen faster* as networks grow — the
transition-width exponent drops from 5.6 to 4.8 under fear.

## 6. How To Intervene (fully spoken — no printed panel; cut for space in
the final layout, the claims live here)

So where do you spend a calming intervention — reassurance, liquidity,
deposit guarantees? Three verified answers, and then the punchline.

**Cap the concentration** — on a lighter-tailed network, no mega-hubs,
bounded shocks simply never ignited: zero systemic events in sixteen
thousand trials, at any fear level. **Calm the hubs** — lowering fear at
high-degree nodes strictly beats the same effort at the periphery. And
**contain the news, not the neighbors** — fear confined near the crisis is
statistically indistinguishable from no fear at all; only network-wide fear
accelerates collapse.

And the punchline, from the mechanism: fear right next to an active failure
is nearly harmless — those nodes were going to fail structurally anyway.
The real danger is fear reaching **distant** nodes, where two panicked
failures can pair up and nucleate an entirely *new* front. **Prioritize
calming the regions far from the crisis.**

## 7. Close (The Demo)

**[Point at the big QR box, bottom right — Next Steps is off the print
too, so the SNAP line below is yours to say]**

Everything here is interactive — scan this and the first thing you'll see
is the model itself, then you can watch real precomputed cascades run on
all three network families and see fear start what structure alone never
could. And this is a framework, not a one-off: we're taking it to
real-world SNAP network data next.
