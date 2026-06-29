/* app.js — wires the illustrative engine (cascade.js) to vis-network + controls.
 * Plain <script>; relies on window.Cascade and the global `vis`. */

"use strict";

(function () {
  // fail loudly & visibly if a dependency didn't load, instead of a blank page
  if (typeof vis === "undefined" || !vis.Network) {
    const box = document.getElementById("network");
    if (box) {
      box.innerHTML =
        '<div style="padding:24px;color:#b5640f;font:14px sans-serif">' +
        "Graph library failed to load (<code>vendor/vis-network.min.js</code>). " +
        "Serve the <code>viz/</code> folder over http (e.g. " +
        "<code>python3 -m http.server</code>) or open via GitHub Pages.</div>";
    }
    console.error("[cascade demo] vis-network not loaded");
    return;
  }

  const { runCascade, CHANNEL } = window.Cascade;

  // color per channel (must match the CSS legend chips).
  // NOTE: vis-network node color uses { background, border } — not { bg, ... }.
  const COLORS = {
    [CHANNEL.SOLVENT]: { background: "#064e3b", border: "#10b981" },
    [CHANNEL.SEED]: { background: "#475569", border: "#94a3b8" },
    [CHANNEL.SOLVENCY]: { background: "#78350f", border: "#f59e0b" },
    [CHANNEL.FEAR]: { background: "#7f1d1d", border: "#ef4444" },
  };

  const THETA = 0.5; // systemic-event threshold (tracker §3.5 default)
  const PLAY_MS = 650; // ms per round during Play

  // ---- DOM handles ----
  const el = (id) => document.getElementById(id);
  const controls = {
    r: el("in-r"), mu: el("in-mu"), kappa: el("in-kappa"),
    a: el("in-a"), p: el("in-p"), n: el("in-n"), seed: el("in-seed"),
  };
  const vals = {
    r: el("val-r"), mu: el("val-mu"), kappa: el("val-kappa"),
    a: el("val-a"), p: el("val-p"), n: el("val-n"),
  };
  const stat = {
    round: el("stat-round"), at: el("stat-at"), frac: el("stat-frac"),
    systemic: el("stat-systemic"), g: el("stat-g"), thermo: el("thermo-fill"),
  };

  // ---- state ----
  let network = null;
  let nodesDS = null;
  let edgesDS = null;
  let trace = null;       // current cascade trace
  let stepIdx = 0;        // index into trace.rounds revealed so far
  let maxG = 0;           // run-max panic field, for thermometer scaling
  let playTimer = null;

  function readParams() {
    return {
      r: parseInt(controls.r.value, 10),
      mu: parseFloat(controls.mu.value),
      kappa: parseFloat(controls.kappa.value),
      a: parseInt(controls.a.value, 10),
      p: parseFloat(controls.p.value),
      n: parseInt(controls.n.value, 10),
      seed: parseInt(controls.seed.value, 10) || 0,
    };
  }

  function syncValueLabels(pr) {
    vals.r.textContent = pr.r;
    vals.mu.textContent = pr.mu.toFixed(2);
    vals.kappa.textContent = pr.kappa.toFixed(1);
    vals.a.textContent = pr.a;
    vals.p.textContent = pr.p.toFixed(3);
    vals.n.textContent = pr.n;
  }

  function buildNetwork(pr) {
    nodesDS = new vis.DataSet(
      Array.from({ length: pr.n }, (_, i) => ({
        id: i,
        color: COLORS[CHANNEL.SOLVENT],
        size: 10,
      }))
    );
    edgesDS = new vis.DataSet(
      trace.edges.map(([a, b], k) => ({ id: k, from: a, to: b }))
    );
    const data = { nodes: nodesDS, edges: edgesDS };
    const options = {
      nodes: { shape: "dot", borderWidth: 1.5,
        font: { size: 0 } },
      edges: { color: { color: "rgba(148, 163, 184, 0.2)", highlight: "#f59e0b" }, width: 0.6,
        smooth: false },
      physics: {
        enabled: true,
        stabilization: { enabled: true, iterations: 220, fit: true },
        barnesHut: { gravitationalConstant: -3500, springLength: 70,
          springConstant: 0.04, avoidOverlap: 0.2 },
      },
      interaction: { dragNodes: true, zoomView: true, hover: true },
    };
    if (network) network.destroy();
    network = new vis.Network(el("network"), data, options);
    // Lay the graph out once, then FREEZE physics so nodes hold still during the
    // cascade animation (recoloring/resizing nodes won't jiggle the layout).
    // Dragging a node still works; it just stays where you drop it.
    network.once("stabilizationIterationsDone", function () {
      network.setOptions({ physics: false });
    });
  }

  // recompute everything from current controls
  function rebuild() {
    stopPlay();
    const pr = readParams();
    // a cannot exceed n
    if (pr.a > pr.n) { pr.a = pr.n; controls.a.value = pr.n; }
    syncValueLabels(pr);
    trace = runCascade(pr);
    maxG = trace.rounds.reduce((m, rd) => Math.max(m, rd.g), 0) || 1;
    buildNetwork(pr);
    stepIdx = 0;
    applyRound(0);
  }

  // reveal rounds 0..k and update the readout to round k
  function applyRound(k) {
    if (!trace) return;
    k = Math.max(0, Math.min(k, trace.rounds.length - 1));
    stepIdx = k;

    // color every node by its channel IF it has failed by round k, else solvent
    const updates = [];
    for (let i = 0; i < trace.n; i++) {
      const fr = trace.failRound[i];
      const revealed = fr >= 0 && fr <= k;
      const ch = revealed ? trace.failChannel[i] : CHANNEL.SOLVENT;
      updates.push({ id: i, color: COLORS[ch], size: revealed ? 13 : 10 });
    }
    nodesDS.update(updates);

    const rd = trace.rounds[k];
    const fracSoFar = rd.A / trace.n;
    stat.round.textContent = rd.t;
    stat.at.textContent = rd.a_t;
    stat.frac.textContent = fracSoFar.toFixed(3);
    stat.g.textContent = rd.g.toFixed(3);
    stat.thermo.style.width = (100 * (rd.g / maxG)).toFixed(1) + "%";

    const atEnd = k === trace.rounds.length - 1;
    if (atEnd) {
      const sys = trace.finalFraction >= THETA;
      stat.systemic.textContent = sys ? "YES" : "no";
      stat.systemic.className = "v " + (sys ? "yes" : "nope");
    } else {
      stat.systemic.textContent = "—";
      stat.systemic.className = "v";
    }
  }

  function stepForward() {
    if (!trace) return;
    if (stepIdx >= trace.rounds.length - 1) { stopPlay(); return; }
    applyRound(stepIdx + 1);
  }

  function play() {
    if (!trace) return;
    if (stepIdx >= trace.rounds.length - 1) applyRound(0); // replay from start
    el("btn-play").innerHTML = "&#10073;&#10073; Pause";
    playTimer = setInterval(() => {
      if (stepIdx >= trace.rounds.length - 1) { stopPlay(); return; }
      stepForward();
    }, PLAY_MS);
  }

  function stopPlay() {
    if (playTimer) { clearInterval(playTimer); playTimer = null; }
    el("btn-play").innerHTML = "&#9654; Play";
  }

  function togglePlay() { playTimer ? stopPlay() : play(); }

  // ---- listeners ----
  Object.values(controls).forEach((c) => {
    // live label while dragging
    c.addEventListener("input", () => syncValueLabels(readParams()));
    // rebuild on commit (release / change)
    c.addEventListener("change", rebuild);
  });

  el("btn-play").addEventListener("click", togglePlay);
  el("btn-step").addEventListener("click", () => { stopPlay(); stepForward(); });
  el("btn-reset").addEventListener("click", () => { stopPlay(); applyRound(0); });
  el("btn-reroll").addEventListener("click", () => {
    controls.seed.value = Math.floor(Math.random() * 1e9);
    rebuild();
  });

  // ---- go ----
  rebuild();
})();
