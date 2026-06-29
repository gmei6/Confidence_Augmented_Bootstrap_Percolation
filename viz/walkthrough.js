/* walkthrough.js — the GUIDED-WALKTHROUGH step-trace engine.
 *
 * WT_EXAMPLE (Part A): 7 nodes, seed A(0) = {1,4}, r = 2, fear off (μ = 0).
 *   Reproduces the deck's worked example exactly (slides 7–10).
 *   Purpose: illustrate the Janson FIFO reformulation; show the two-channel
 *   model is a strict add-on that reduces to Janson at μ = 0.
 *
 * WT_PART_B (Part B): same graph, seed A(0) = {1} only, r = 2, μ = 0.85.
 *   Purpose: show how the fear channel enables a cascade from a single seed
 *   that Janson alone cannot propagate (S(0)=∅ → halt at μ=0).
 *   Fear and Bernoulli outcomes are pre-determined so the example is
 *   deterministic and matches a fixed narrative.
 *
 * ILLUSTRATIVE — a teaching reimplementation, not the validated oracle.
 */

"use strict";

// ---- Part A: the deck's fixed example (must match slides 7–10) ----
const WT_EXAMPLE = {
  n: 7,
  edges: [
    [1, 2], [1, 3], [1, 5], [2, 4], [2, 6],
    [3, 4], [3, 7], [4, 5], [5, 6], [6, 7],
  ],
  seed: [1, 4],
  r: 2,
  mu: 0,
  // node layout copied from the slide (normalized 0..1, y-down)
  pos: {
    1: [0.733, 0.487], 2: [0.251, 0.046], 3: [0.606, 1.000], 4: [0.216, 1.000],
    5: [0.000, 0.394], 6: [0.618, 0.000], 7: [1.000, 0.440],
  },
};

// ---- Part B: same graph, single seed, high fear ----
// Individual fear values fi pre-drawn from Beta(μκ,(1-μ)κ) with μ=0.85, κ=20.
// Bernoulli outcomes are fixed so the walkthrough is deterministic:
//   Gen 0 fear (g₁=1/7≈0.143):  F(0) = {2,6}
//   Gen 1 fear (g₂=2/7≈0.286):  F(1) = {3}
//   Gen 2 and beyond: no solvent nodes remain → F(k)=∅
// Result: all 7 banks fail — |A*|/n = 1.0 from a single seed.
const WT_PART_B = {
  n: 7,
  edges: [
    [1, 2], [1, 3], [1, 5], [2, 4], [2, 6],
    [3, 4], [3, 7], [4, 5], [5, 6], [6, 7],
  ],
  seed: [1],
  r: 2,
  mu: 0.85,
  kappa: 20,
  fearValues: { 2: 0.90, 3: 0.80, 4: 0.85, 5: 0.88, 6: 0.92, 7: 0.83 },
  fearOutcomes: { 0: [2, 6], 1: [3] }, // missing keys → []
  // U_i ~ Uniform(0,1) pre-drawn per solvent node per generation.
  // Node i fails if U_i < f_i * g_{k+1}.
  fearBernoulli: {
    0: { 2: 0.08, 3: 0.62, 4: 0.44, 5: 0.71, 6: 0.09, 7: 0.55 },
    1: { 3: 0.14, 4: 0.56, 7: 0.51 },
  },
  pos: {
    1: [0.733, 0.487], 2: [0.251, 0.046], 3: [0.606, 1.000], 4: [0.216, 1.000],
    5: [0.000, 0.394], 6: [0.618, 0.000], 7: [1.000, 0.440],
  },
};

function setStr(arr) { return "{" + arr.slice().sort((a, b) => a - b).join(",") + "}"; }
function emptyOr(arr) { return arr.length ? setStr(arr) : "∅"; }

/**
 * Build the full granular frame list for a walkthrough example.
 *
 * Returns { n, edges, frames, columns, hasFear } where each frame is:
 *   { type, k, caption,
 *     table:  [ {node, fi, marks, active, used, gen, channel} ... ],
 *     row:    {t, u, k, Tk, Z, A, g, S, F} | null,
 *     hi:     { processing, newMarks, solvency, fear } }
 *
 * If cfg contains fearValues/fearOutcomes, the fear channel is exercised with
 * pre-determined Bernoulli outcomes and detailed per-node probability captions.
 */
function buildWalkthrough(cfg) {
  cfg = cfg || WT_EXAMPLE;
  const { n, edges, seed, r, mu } = cfg;
  const fearValues = cfg.fearValues || null;      // { nodeId: fi, ... }
  const fearOutcomes = cfg.fearOutcomes || null;  // { genK: [nodeIds], ... }
  const fearBernoulli = cfg.fearBernoulli || null; // { genK: { nodeId: U_i }, ... }
  const kappa = cfg.kappa || null;

  const adj = Array.from({ length: n + 1 }, () => []);
  for (const [a, b] of edges) { adj[a].push(b); adj[b].push(a); }

  const marks = new Array(n + 1).fill(0);
  const active = new Array(n + 1).fill(false);
  const used = new Array(n + 1).fill(false);
  const gen = new Array(n + 1).fill(null);
  const channel = new Array(n + 1).fill(null);

  const frames = [];
  const Z = [];
  let t = 0;
  let curGenPrevNew = 0;

  function snapshot() {
    const tbl = [];
    for (let i = 1; i <= n; i++) {
      tbl.push({
        node: i,
        // fi: always show the fixed value (or null if seed has no entry)
        fi: fearValues ? (fearValues[i] !== undefined ? fearValues[i] : null) : undefined,
        marks: active[i] ? null : marks[i],
        active: active[i],
        used: used[i],
        gen: gen[i],
        channel: channel[i],
      });
    }
    return tbl;
  }
  function activeSet() {
    const s = []; for (let i = 1; i <= n; i++) if (active[i]) s.push(i); return s;
  }

  // ---- generation 0: the seed ----
  let k = 0;
  for (const s of seed) { active[s] = true; gen[s] = 0; channel[s] = "seed"; }
  let Tk = seed.length;
  let queue = seed.slice();
  let curGenNew = seed.length;

  // Build init caption — Part B variant names the fi values
  let initCaption;
  if (fearValues && kappa) {
    const fList = Object.keys(fearValues)
      .map(Number).sort((a, b) => a - b)
      .map((i) => `f<sub>${i}</sub>&thinsp;=&thinsp;${fearValues[i].toFixed(2)}`).join(", ");
    initCaption =
      `Initialize generation k = 0: seed A(0) = ${setStr(seed)} — a single initial failure. ` +
      `Individual fear values f<sub>i</sub>&thinsp;~&thinsp;Beta(μκ,&thinsp;(1&minus;μ)κ) ` +
      `with μ = ${mu}, κ = ${kappa}, drawn once at t = 0: ${fList}. ` +
      `Used set Z = ∅, threshold r = ${r}.`;
  } else {
    initCaption =
      `Initialize generation k = 0: seed the shock A(0) = ${setStr(seed)} as ` +
      `failed (active, gen 0). Used set Z = ∅, threshold r = ${r}. ` +
      `Every other node has 0 marks.`;
  }

  frames.push({
    type: "init", k: 0,
    caption: initCaption,
    caption_layperson: fearValues && kappa
      ? `Initialize the crisis: Bank 1 collapses due to an initial economic shock. The other banks (2 to 7) have different anxiety levels (shown in the table below), representing how vulnerable they are to public panic.`
      : `Initialize the crisis: Banks ${setStr(seed)} collapse due to an initial shock and enter the failure queue. Warning marks on all other banks are at 0.`,
    table: snapshot(), row: null,
    hi: { processing: null, newMarks: [], solvency: [], fear: [] },
  });

  let guard = 0;
  while (queue.length && guard++ < 1000) {
    const layer = queue;
    queue = [];
    let lastRow = null;

    for (const u of layer) {
      t += 1;
      used[u] = true;
      Z.push(u);
      const newMarks = [];
      for (const v of adj[u]) {
        if (!active[v]) { marks[v] += 1; newMarks.push([u, v]); }
      }
      const row = {
        t, u: setStr([u]), k, Tk, Z: setStr(Z), A: setStr(activeSet()),
        g: k === 0 ? "0" : `${curGenPrevNew}/${n}`,
        S: "—", F: "—",
      };
      lastRow = row;
      frames.push({
        type: "process", k,
        caption:
          `Step t = ${t}: pop node ${u} from the front of the active queue and ` +
          `add it to the used set Z. It marks its still-solvent neighbors ` +
          (newMarks.length ? `(${newMarks.map((e) => e[1]).join(", ")})` : "(none)") +
          ` — each gains one failed-neighbor mark.`,
        caption_layperson:
          `Step ${t}: We examine Bank ${u} (shown in yellow). Since it has failed, it puts stress on its ` +
          `business partners ` +
          (newMarks.length ? `(Banks ${newMarks.map((e) => e[1]).join(", ")})` : "(none)") +
          `. We add one warning mark (orange border) to each of them.`,
        table: snapshot(),
        row,
        hi: { processing: u, newMarks, solvency: [], fear: [] },
      });
    }

    // ---- (a) solvency: solvent nodes that reached >= r marks fail ----
    const Sk = [];
    for (let i = 1; i <= n; i++) if (!active[i] && marks[i] >= r) Sk.push(i);
    for (const i of Sk) { active[i] = true; gen[i] = k + 1; channel[i] = "solvency"; }
    if (lastRow) lastRow.S = emptyOr(Sk);

    // Extra note for Part B gen-0: solvency alone can't propagate from a single seed
    let solvencyNote = "";
    if (Sk.length === 0 && mu > 0 && k === 0) {
      solvencyNote = " With μ = 0 (Janson alone), the cascade would halt here — the fear channel takes over next.";
    }
    frames.push({
      type: "solvency", k,
      caption: Sk.length
        ? `Generation ${k} fully processed (step ${t} = T_k). Solvency check: ` +
          `nodes ${Sk.join(", ")} reached r = ${r} marks and fail by solvency, ` +
          `S(${k}) = ${setStr(Sk)}.`
        : `Generation ${k} fully processed (step ${t} = T_k). Solvency check: ` +
          `no solvent node has reached r = ${r} marks, S(${k}) = ∅.${solvencyNote}`,
      caption_layperson:
        `Check the domino effect: Do any healthy banks have ${r} or more failed partners? ` +
        (Sk.length
          ? `Yes! Banks ${Sk.join(", ")} reached the limit of ${r} warning marks and collapse (turning orange).`
          : `No healthy bank has reached ${r} warning marks, so none collapse in this step.` +
            (mu > 0 && k === 0 ? ` With the domino effect alone, the cascade would stop here; however, public panic is about to play a role.` : "")),
      table: snapshot(), row: null,
      hi: { processing: null, newMarks: [], solvency: Sk, fear: [] },
    });

    // ---- (b) fear: compute g_{k+1} = a_k / n ----
    const g = curGenNew / n;

    // Collect solvent nodes before fear marks them active (for caption detail)
    const solventBeforeFear = [];
    for (let i = 1; i <= n; i++) { if (!active[i]) solventBeforeFear.push(i); }

    const Fk = fearOutcomes ? (fearOutcomes[k] || []) : [];
    for (const i of Fk) { active[i] = true; gen[i] = k + 1; channel[i] = "fear"; }
    if (lastRow) lastRow.F = emptyOr(Fk);

    // Build fear caption
    const bDraws = fearBernoulli ? (fearBernoulli[k] || null) : null;
    // f_i * g for each solvent node — shown in the table on fear frames
    const fearProbs = {};
    if (fearValues) {
      for (const i of solventBeforeFear) {
        fearProbs[i] = (fearValues[i] !== undefined ? fearValues[i] : 0) * g;
      }
    }
    let fearCaption;
    if (mu > 0 && fearValues && solventBeforeFear.length > 0) {
      // Per-node breakdown: show U_i draw when available, else show probability
      const details = solventBeforeFear.map((i) => {
        const fi = fearValues[i] !== undefined ? fearValues[i] : 0;
        const p = fi * g;
        const failed = Fk.includes(i);
        if (bDraws && bDraws[i] !== undefined) {
          const u = bDraws[i];
          const cmp = failed
            ? `U<sub>${i}</sub>=<strong>${u.toFixed(3)}</strong> &lt; f<sub>${i}</sub>&thinsp;&middot;&thinsp;g&thinsp;=&thinsp;${p.toFixed(3)}`
            : `U<sub>${i}</sub>=${u.toFixed(3)} &ge; f<sub>${i}</sub>&thinsp;&middot;&thinsp;g&thinsp;=&thinsp;${p.toFixed(3)}`;
          return `node ${i}: ${cmp} &rarr; ${failed ? "<strong>fails</strong>" : "survives"}`;
        }
        return `node ${i}: ${fi.toFixed(2)}&thinsp;&times;&thinsp;${g.toFixed(3)}&thinsp;=&thinsp;${p.toFixed(3)} &rarr; ${failed ? "<strong>fails</strong>" : "survives"}`;
      }).join("; ");
      const drawPhrase = bDraws
        ? `Each still-solvent bank i draws U<sub>i</sub>&thinsp;~&thinsp;Uniform(0,1) and fails if U<sub>i</sub> &lt; f<sub>i</sub>&thinsp;&middot;&thinsp;g<sub>${k + 1}</sub>:`
        : `Each still-solvent bank i draws Bernoulli(f<sub>i</sub>&thinsp;&times;&thinsp;g<sub>${k + 1}</sub>):`;
      fearCaption =
        `Panic field g<sub>${k + 1}</sub> = a<sub>${k}</sub>/n = ${curGenNew}/${n} &asymp; ${g.toFixed(3)}. ` +
        `${drawPhrase} ${details}. F(${k}) = ${emptyOr(Fk)}.`;
    } else if (mu > 0 && fearValues && solventBeforeFear.length === 0) {
      fearCaption =
        `Panic field g<sub>${k + 1}</sub> = a<sub>${k}</sub>/n = ${curGenNew}/${n} ≈ ${g.toFixed(3)}. ` +
        `All banks have already failed — no solvent nodes remain. F(${k}) = ∅.`;
    } else {
      fearCaption =
        `Compute the panic field g_${k + 1} = a_${k}/n = ${curGenNew}/${n} = ` +
        `${g.toFixed(3)}. ` +
        (mu > 0
          ? `Each remaining solvent bank fails w.p. f_i·g; fear failures ` +
            `F(${k}) = ${emptyOr(Fk)}.`
          : `This example has μ = 0, so every f_i = 0 and no fear failures ` +
            `occur: F(${k}) = ∅.`);
    }

    frames.push({
      type: "fear", k,
      bernoulliDraws: bDraws,                                        // { nodeId: U_i } for this gen, or null
      fearProbs: Object.keys(fearProbs).length ? fearProbs : null,   // { nodeId: f_i*g } for this gen, or null
      caption: fearCaption,
      caption_layperson:
        `Check for crowd panic: ${curGenNew} out of ${n} banks failed last round, so the panic level ` +
        `is ${(g * 100).toFixed(1)}%. ` +
        (mu > 0
          ? `Each remaining bank has a chance to fail purely due to panic. Fear failures: ${emptyOr(Fk)}.`
          : `Since fear is turned off in this demo, no banks fail from panic.`),
      table: snapshot(), row: null,
      hi: { processing: null, newMarks: [], solvency: [], fear: Fk },
    });

    // ---- (c) union: new failures join the active queue as generation k+1 ----
    const newAct = Sk.concat(Fk);
    curGenPrevNew = curGenNew;
    curGenNew = newAct.length;
    if (newAct.length) {
      queue = newAct.slice();
      Tk += newAct.length;
      k += 1;
      frames.push({
        type: "union", k,
        caption:
          `Union: S(${k - 1}) ∪ F(${k - 1}) = ${setStr(newAct)} become ` +
          `generation ${k} and enter the queue. T_k advances to ${Tk}. ` +
          `Continue processing.`,
        caption_layperson:
          `The newly collapsed banks ${setStr(newAct)} now become the new sources of stress. ` +
          `We will process them one by one in the next generation.`,
        table: snapshot(), row: null,
        hi: { processing: null, newMarks: [], solvency: [], fear: [] },
      });
    } else {
      frames.push({
        type: "halt", k,
        caption:
          `No new failures this generation — the cascade halts. Final failed ` +
          `set A* has ${activeSet().length} of ${n} banks ` +
          `(|A*|/n = ${(activeSet().length / n).toFixed(3)}).`,
        caption_layperson:
          `No more banks failed in this round — the chain reaction stops. ` +
          `In this run, a total of ${activeSet().length} out of ${n} banks ended up collapsing ` +
          `(${(activeSet().length / n * 100).toFixed(1)}% of the network).`,
        table: snapshot(), row: null,
        hi: { processing: null, newMarks: [], solvency: [], fear: [] },
      });
    }
  }

  return {
    n, edges, frames,
    columns: ["t", "u_t", "k(t)", "T_k(t)", "Z(t)", "A(t)", "g_k(t)", "S(k)", "F(k)"],
    hasFear: mu > 0,
  };
}

if (typeof window !== "undefined") {
  window.Walkthrough = { buildWalkthrough, WT_EXAMPLE, WT_PART_B };
}
if (typeof module !== "undefined") module.exports = { buildWalkthrough, WT_EXAMPLE, WT_PART_B };
