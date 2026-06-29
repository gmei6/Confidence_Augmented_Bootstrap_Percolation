/* walkthrough.js — the GUIDED-WALKTHROUGH step-trace engine.
 *
 * Reproduces the deck's worked example EXACTLY (slides 7–10):
 *   7 nodes, seed A(0) = {1,4}, r = 2, fear off (mu = 0, solvency-led).
 * Edges extracted from the PowerPoint connector shapes.
 *
 * Unlike cascade.js (which emits round-level summaries), this decomposes the
 * Janson FIFO reformulation (tracker §5.1 / S-019) into granular, captioned
 * sub-steps and tracks the deck's Node / Marks / Active? / Gen table plus the
 * t / u_t / k(t) / T_{k(t)} / Z(t) / A(t) / g_{k(t)} / S(k) / F(k) step table.
 *
 * ILLUSTRATIVE — a teaching reimplementation, not the validated oracle.
 */

"use strict";

// ---- the deck's fixed example (do not randomize: it must match the slides) ----
const WT_EXAMPLE = {
  n: 7,
  edges: [
    [1, 2], [1, 3], [1, 5], [2, 4], [2, 6],
    [3, 4], [3, 7], [4, 5], [5, 6], [6, 7],
  ],
  seed: [1, 4], // A(0)
  r: 2,
  mu: 0, // solvency-led example (fear off) — matches the deck's shown g=0, F=empty
  // node layout copied from the slide (normalized 0..1, y-down) so the web graph
  // matches the deck's arrangement
  pos: {
    1: [0.733, 0.487], 2: [0.251, 0.046], 3: [0.606, 1.000], 4: [0.216, 1.000],
    5: [0.000, 0.394], 6: [0.618, 0.000], 7: [1.000, 0.440],
  },
};

function setStr(arr) { return "{" + arr.slice().sort((a, b) => a - b).join(",") + "}"; }
function emptyOr(arr) { return arr.length ? setStr(arr) : "∅"; } // ∅

/**
 * Build the full granular frame list for the fixed example.
 *
 * Returns { n, edges, frames, columns } where each frame is:
 *   { type, k, caption,
 *     table:  [ {node, marks, active, used, gen} ... ]   // full snapshot
 *     row:    {t, u, k, Tk, Z, A, g, S, F} | null,        // step-table row (process frames)
 *     hi:     { processing, newMarks:[[u,v]...], solvency:[], fear:[] } }
 */
function buildWalkthrough(cfg) {
  cfg = cfg || WT_EXAMPLE;
  const { n, edges, seed, r, mu } = cfg;

  // adjacency (1-indexed)
  const adj = Array.from({ length: n + 1 }, () => []);
  for (const [a, b] of edges) { adj[a].push(b); adj[b].push(a); }

  // per-node state
  const marks = new Array(n + 1).fill(0);
  const active = new Array(n + 1).fill(false);
  const used = new Array(n + 1).fill(false);
  const gen = new Array(n + 1).fill(null);
  const channel = new Array(n + 1).fill(null); // 'seed' | 'solvency' | 'fear'

  const frames = [];
  const Z = []; // used set, in processing order
  let t = 0;    // step counter (one per processed node)
  let curGenPrevNew = 0; // a_{k-1} for the g-column display on generation k's rows

  function snapshot() {
    const tbl = [];
    for (let i = 1; i <= n; i++) {
      tbl.push({
        node: i,
        // the deck shows "—" for marks of already-active nodes
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
  let Tk = seed.length;             // T_0 = number of gen-0 nodes
  let queue = seed.slice();         // FIFO of active-but-unused nodes
  let curGenNew = seed.length;      // a_0 = |new failures this generation| (the seed)

  frames.push({
    type: "init", k: 0,
    caption:
      `Initialize generation k = 0: seed the shock A(0) = ${setStr(seed)} as ` +
      `failed (active, gen 0). Used set Z = ∅, threshold r = ${r}. ` +
      `Every other node has 0 marks.`,
    table: snapshot(), row: null,
    hi: { processing: null, newMarks: [], solvency: [], fear: [] },
  });

  let guard = 0;
  while (queue.length && guard++ < 1000) {
    // process every node currently queued for THIS generation layer
    const layer = queue;
    queue = [];
    let lastRow = null; // the generation's final step row, gets S(k)/F(k) backfilled

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
        S: "—", F: "—", // backfilled at generation end
      };
      lastRow = row;
      frames.push({
        type: "process", k,
        caption:
          `Step t = ${t}: pop node ${u} from the front of the active queue and ` +
          `add it to the used set Z. It marks its still-solvent neighbors ` +
          (newMarks.length ? `(${newMarks.map((e) => e[1]).join(", ")})` : "(none)") +
          ` — each gains one failed-neighbor mark.`,
        table: snapshot(),
        row,
        hi: { processing: u, newMarks, solvency: [], fear: [] },
      });
    }

    // ---- generation boundary: resolve solvency, then fear, then union ----
    // (a) solvency: solvent nodes that reached >= r marks fail
    const Sk = [];
    for (let i = 1; i <= n; i++) if (!active[i] && marks[i] >= r) Sk.push(i);
    for (const i of Sk) { active[i] = true; gen[i] = k + 1; channel[i] = "solvency"; }
    if (lastRow) lastRow.S = emptyOr(Sk);

    frames.push({
      type: "solvency", k,
      caption:
        `Generation ${k} fully processed (step ${t} = T_k). Solvency check: ` +
        (Sk.length
          ? `nodes ${Sk.join(", ")} reached r = ${r} marks and fail by solvency, ` +
            `S(${k}) = ${setStr(Sk)}.`
          : `no solvent node has reached r = ${r} marks, S(${k}) = ∅.`),
      table: snapshot(),
      row: null,
      hi: { processing: null, newMarks: [], solvency: Sk, fear: [] },
    });

    // (b) fear: compute g_{k+1} = a_k / n, draw fear for remaining solvent nodes
    const g = curGenNew / n;
    const Fk = [];
    if (mu > 0) {
      // (not exercised in the deck's mu=0 example; kept for completeness)
      for (let i = 1; i <= n; i++) {
        if (!active[i]) { /* would draw Bernoulli(f_i * g); omitted at mu=0 */ }
      }
    }
    for (const i of Fk) { active[i] = true; gen[i] = k + 1; channel[i] = "fear"; }
    if (lastRow) lastRow.F = emptyOr(Fk);

    frames.push({
      type: "fear", k,
      caption:
        `Compute the panic field g_${k + 1} = a_${k}/n = ${curGenNew}/${n} = ` +
        `${g.toFixed(3)}. ` +
        (mu > 0
          ? `Each remaining solvent bank fails w.p. f_i·g; fear failures ` +
            `F(${k}) = ${emptyOr(Fk)}.`
          : `This example has μ = 0, so every f_i = 0 and no fear failures ` +
            `occur: F(${k}) = ∅.`),
      table: snapshot(),
      row: null,
      hi: { processing: null, newMarks: [], solvency: [], fear: Fk },
    });

    // (c) union: new failures join the active queue as generation k+1
    const newAct = Sk.concat(Fk);
    curGenPrevNew = curGenNew;   // remember for g display on next layer's rows
    curGenNew = newAct.length;
    if (newAct.length) {
      queue = newAct.slice();
      Tk += newAct.length;       // T_{k+1}
      k += 1;
      frames.push({
        type: "union", k,
        caption:
          `Union: S(${k - 1}) ∪ F(${k - 1}) = ${setStr(newAct)} become ` +
          `generation ${k} and enter the queue. T_k advances to ${Tk}. ` +
          `Continue processing.`,
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
        table: snapshot(), row: null,
        hi: { processing: null, newMarks: [], solvency: [], fear: [] },
      });
    }
  }

  return {
    n, edges, frames,
    columns: ["t", "u_t", "k(t)", "T_k(t)", "Z(t)", "A(t)", "g_k(t)", "S(k)", "F(k)"],
  };
}

if (typeof window !== "undefined") {
  window.Walkthrough = { buildWalkthrough, WT_EXAMPLE };
}
if (typeof module !== "undefined") module.exports = { buildWalkthrough, WT_EXAMPLE };
