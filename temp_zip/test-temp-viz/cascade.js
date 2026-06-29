/* cascade.js — ILLUSTRATIVE in-browser engine for the two-channel cascade demo.
 *
 * This is NOT the validated engine. The source of truth is
 * src/twocascade/reference.py (the oracle); the research results come from the
 * C++ core validated against it (§5.4). This file faithfully mirrors the §3.4
 * dynamics for *teaching at small n*, and is deliberately not cross-validated.
 *
 * Model (tracker §3):
 *   - Graph: Erdos-Renyi G(n,p).
 *   - Channel 1 (solvency, Janson): a solvent bank fails if >= r neighbors failed.
 *   - Channel 2 (fear): solvent bank i fails w.p. f_i * g_t, where the global
 *     panic field g_t = a_{t-1}/n is INCREMENTAL (last round's new-failure rate),
 *     and f_i ~ Beta(mu*kappa, (1-mu)*kappa) drawn once at t=0 so E[f]=mu.
 *   - Updates are SIMULTANEOUS: evaluate all banks against frozen state, then
 *     mutate. Halt when a round produces no new failures.
 */

"use strict";

/* ---- seeded RNG (mulberry32): reproducible given the seed field ---- */
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ---- standard normal via Box-Muller ---- */
function sampleNormal(rng) {
  let u = 0, v = 0;
  while (u === 0) u = rng();
  while (v === 0) v = rng();
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
}

/* ---- Gamma(shape, scale=1) via Marsaglia-Tsang ---- */
function sampleGamma(rng, shape) {
  if (shape <= 0) return 0;
  if (shape < 1) {
    // boost: Gamma(shape) = Gamma(shape+1) * U^(1/shape)
    const u = rng();
    return sampleGamma(rng, shape + 1) * Math.pow(u, 1 / shape);
  }
  const d = shape - 1 / 3;
  const c = 1 / Math.sqrt(9 * d);
  while (true) {
    let x, v;
    do {
      x = sampleNormal(rng);
      v = 1 + c * x;
    } while (v <= 0);
    v = v * v * v;
    const u = rng();
    if (u < 1 - 0.0331 * x * x * x * x) return d * v;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
  }
}

/* ---- Beta(alpha, beta) via two Gammas, with mu=0 / mu=1 guards (LESSONS §2) ---- */
function sampleBeta(rng, alpha, beta) {
  if (alpha <= 0) return 0; // mu = 0  -> f_i = 0 (Janson baseline, fear off)
  if (beta <= 0) return 1;  // mu = 1  -> f_i = 1
  const y1 = sampleGamma(rng, alpha);
  const y2 = sampleGamma(rng, beta);
  const s = y1 + y2;
  return s > 0 ? y1 / s : 0;
}

/* ---- channel labels (also the color keys used by index.html) ---- */
const CHANNEL = { SEED: "seed", SOLVENCY: "solvency", FEAR: "fear", SOLVENT: "solvent" };

/**
 * Run one illustrative cascade and return its full trace for animation.
 *
 * params: { n, p, r, mu, kappa, a, seed }
 * returns: {
 *   n, edges:[[i,j],...], failRound:Int[], failChannel:String[],
 *   rounds:[{ t, newNodes:[{node,channel}], g, a_t, A }],
 *   finalA, finalFraction
 * }
 */
function runCascade(params) {
  const { n, p, r, mu, kappa, a, seed } = params;
  const rng = mulberry32(seed);

  // --- G(n,p): sample each unordered pair (O(n^2); fine for n <= ~150) ---
  const adj = Array.from({ length: n }, () => []);
  const edges = [];
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      if (rng() < p) {
        adj[i].push(j);
        adj[j].push(i);
        edges.push([i, j]);
      }
    }
  }

  // --- individual fear f_i ~ Beta(mu*kappa, (1-mu)*kappa), drawn once ---
  const alpha = mu * kappa;
  const betaParam = (1 - mu) * kappa;
  const f = new Array(n);
  for (let i = 0; i < n; i++) f[i] = sampleBeta(rng, alpha, betaParam);

  // --- state ---
  const failed = new Array(n).fill(false);
  const failRound = new Array(n).fill(-1);
  const failChannel = new Array(n).fill(CHANNEL.SOLVENT);
  const failedNeighbors = new Array(n).fill(0); // counter, updated only on failure

  // --- seed: a random distinct banks fail at t=0 ---
  const order = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    const k = Math.floor(rng() * (i + 1));
    [order[i], order[k]] = [order[k], order[i]];
  }
  const aClamped = Math.max(0, Math.min(a, n));
  const seedSet = order.slice(0, aClamped);
  const seedNodes = [];
  for (const i of seedSet) {
    failed[i] = true;
    failRound[i] = 0;
    failChannel[i] = CHANNEL.SEED;
    seedNodes.push({ node: i, channel: CHANNEL.SEED });
  }
  for (const i of seedSet) {
    for (const j of adj[i]) failedNeighbors[j]++;
  }

  const rounds = [];
  let A = seedSet.length;
  let prevNew = seedSet.length; // a_0 = a
  rounds.push({ t: 0, newNodes: seedNodes, g: 0, a_t: seedSet.length, A });

  // --- dynamics ---
  let t = 0;
  const MAX_ROUNDS = 10000; // safety; the process is monotone and must halt
  while (t < MAX_ROUNDS) {
    t++;
    const g = prevNew / n; // g_t = a_{t-1}/n  (incremental, §3.3)

    // EVALUATE against frozen state (simultaneous update, LESSONS §2)
    const newFails = [];
    for (let i = 0; i < n; i++) {
      if (failed[i]) continue;
      let channel = null;
      if (failedNeighbors[i] >= r) {
        channel = CHANNEL.SOLVENCY; // structural cause takes precedence in coloring
      } else if (rng() < f[i] * g) {
        channel = CHANNEL.FEAR;
      }
      if (channel) newFails.push({ node: i, channel });
    }

    if (newFails.length === 0) break;

    // MUTATE
    for (const { node, channel } of newFails) {
      failed[node] = true;
      failRound[node] = t;
      failChannel[node] = channel;
    }
    for (const { node } of newFails) {
      for (const j of adj[node]) if (!failed[j]) failedNeighbors[j]++;
    }

    A += newFails.length;
    rounds.push({ t, newNodes: newFails, g, a_t: newFails.length, A });
    prevNew = newFails.length;
  }

  return {
    n,
    edges,
    failRound,
    failChannel,
    rounds,
    finalA: A,
    finalFraction: A / n,
  };
}

// expose for index.html (plain <script>, no module system)
window.Cascade = { runCascade, CHANNEL };
