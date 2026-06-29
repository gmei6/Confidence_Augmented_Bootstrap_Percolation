/* tutorial.js — renders the GUIDED WALKTHROUGH (section 3).
 * Drives a fixed-layout vis-network graph + the Node/Marks/Gen table + the
 * t/u_t/k(t)/T_{k(t)}/Z(t)/A(t)/g_{k(t)}/S(k)/F(k) step table, frame by frame,
 * over the trace produced by walkthrough.js. Plain <script>; relies on window.Walkthrough and global `vis`. */

"use strict";

(function () {
  if (typeof window.Walkthrough === "undefined") return;
  const host = document.getElementById("wt-network");
  if (!host) return;
  if (typeof vis === "undefined" || !vis.Network) {
    host.innerHTML =
      '<div style="padding:20px;color:#b5640f">Graph library failed to load.</div>';
    return;
  }

  const { buildWalkthrough, WT_EXAMPLE } = window.Walkthrough;
  const wt = buildWalkthrough();
  const frames = wt.frames;

  // channel fill colors (match cascade.js / the sandbox legend)
  const FILL = {
    seed: "#475569", solvency: "#78350f", fear: "#7f1d1d", solvent: "#064e3b",
  };
  const PROCESSING_RING = "#f59e0b"; // gold
  const MARK_EDGE = "#f59e0b";
  const PLAY_MS = 1100;

  // ---- fixed node layout from the deck (normalized 0..1, y-down) ----
  const SCALE = 230;
  const nodesDS = new vis.DataSet(
    Object.keys(WT_EXAMPLE.pos).map((idStr) => {
      const id = parseInt(idStr, 10);
      const [px, py] = WT_EXAMPLE.pos[id];
      return {
        id, label: String(id),
        x: (px - 0.5) * 2 * SCALE, y: (py - 0.5) * 2 * SCALE,
        fixed: true, physics: false,
        shape: "circle", color: { background: FILL.solvent, border: "#10b981" },
        borderWidth: 2, font: { size: 18, color: "#10b981" },
      };
    })
  );
  const edgesDS = new vis.DataSet(
    wt.edges.map(([a, b], k) => ({
      id: k, from: a, to: b, color: { color: "rgba(148, 163, 184, 0.25)" }, width: 1.2, smooth: false,
    }))
  );

  const network = new vis.Network(
    host,
    { nodes: nodesDS, edges: edgesDS },
    {
      physics: false,
      interaction: { dragNodes: false, zoomView: false, dragView: false },
      nodes: { shape: "circle" },
    }
  );
  network.fit({ animation: false });

  // ---- DOM ----
  const elCaption = document.getElementById("wt-caption");
  const elCounter = document.getElementById("wt-counter");
  const elNodeTable = document.getElementById("wt-node-table");
  const elStepTable = document.getElementById("wt-step-table");
  const btnPrev = document.getElementById("wt-prev");
  const btnNext = document.getElementById("wt-next");
  const btnPlay = document.getElementById("wt-play");
  const btnReset = document.getElementById("wt-reset");

  let idx = 0;
  let timer = null;
  const check = "✓", cross = "✗", dash = "—";

  function renderNodeTable(frame) {
    const isLayperson = document.body.classList.contains("layperson-mode");
    const headers = isLayperson
      ? "<tr><th>Bank</th><th>Warning Marks</th><th>Collapsed?</th><th>Generation</th></tr>"
      : "<tr><th>Node</th><th>Marks</th><th>Active?</th><th>Gen</th></tr>";
    let html = headers;
    for (const r of frame.table) {
      const marks = r.marks === null ? dash : r.marks;
      const act = r.active
        ? `<span class="yes">${isLayperson ? "YES" : check}</span>`
        : `<span class="no">${isLayperson ? "NO" : cross}</span>`;
      const gen = r.gen === null ? dash : r.gen;
      const hi = frame.hi.processing === r.node ? ' class="row-proc"' : "";
      html += `<tr${hi}><td>${r.node}</td><td>${marks}</td><td>${act}</td><td>${gen}</td></tr>`;
    }
    elNodeTable.innerHTML = html;
  }

  function renderStepTable(uptoIdx) {
    const cols = wt.columns;
    let html = "<tr>" + cols.map((c) => `<th>${c}</th>`).join("") + "</tr>";
    for (let i = 0; i <= uptoIdx; i++) {
      const r = frames[i].row;
      if (!r) continue;
      const isLast = i === uptoIdx || !frames.slice(i + 1, uptoIdx + 1).some((f) => f.row);
      html +=
        `<tr${isLast ? ' class="row-current"' : ""}>` +
        `<td>${r.t}</td><td>${r.u}</td><td>${r.k}</td><td>${r.Tk}</td>` +
        `<td>${r.Z}</td><td>${r.A}</td><td>${r.g}</td><td>${r.S}</td><td>${r.F}</td></tr>`;
    }
    elStepTable.innerHTML = html;
  }

  function renderGraph(frame) {
    const nodeUpd = frame.table.map((r) => {
      const fill = r.active ? FILL[r.channel] || FILL.solvency : FILL.solvent;
      const isProc = frame.hi.processing === r.node;
      let border = "#10b981";
      let borderWidth = 2;
      if (r.active && r.used) { border = "#94a3b8"; borderWidth = 3; } // active+used: solid dark
      else if (r.active && !r.used) { border = "#ef4444"; borderWidth = 3; } // active+unused: red ring
      if (isProc) { border = PROCESSING_RING; borderWidth = 6; }
      return {
        id: r.node,
        color: { background: fill, border },
        borderWidth,
        font: { color: r.active ? "#fff" : "#10b981", size: 18 },
      };
    });
    nodesDS.update(nodeUpd);

    // edges: highlight the marks just added this frame
    const marked = new Set(frame.hi.newMarks.map((e) => `${Math.min(e[0], e[1])}-${Math.max(e[0], e[1])}`));
    edgesDS.update(
      wt.edges.map(([a, b], k) => {
        const key = `${Math.min(a, b)}-${Math.max(a, b)}`;
        const on = marked.has(key);
        return { id: k, color: { color: on ? MARK_EDGE : "rgba(148, 163, 184, 0.25)" }, width: on ? 3 : 1.2 };
      })
    );
  }

  function render() {
    const frame = frames[idx];
    renderGraph(frame);
    renderNodeTable(frame);
    renderStepTable(idx);

    const isLayperson = document.body.classList.contains("layperson-mode");
    const caption = isLayperson && frame.caption_layperson ? frame.caption_layperson : frame.caption;

    elCaption.innerHTML = `<span class="wt-tag tag-${frame.type}">${frame.type}</span> ${caption}`;
    elCounter.textContent = `frame ${idx + 1} / ${frames.length}`;
    btnPrev.disabled = idx === 0;
    btnNext.disabled = idx === frames.length - 1;
  }

  function go(i) {
    idx = Math.max(0, Math.min(i, frames.length - 1));
    render();
  }
  function next() {
    if (idx >= frames.length - 1) { stop(); return; }
    go(idx + 1);
  }
  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
    btnPlay.innerHTML = "&#9654; Play";
  }
  function play() {
    if (idx >= frames.length - 1) go(0);
    btnPlay.innerHTML = "&#10073;&#10073; Pause";
    timer = setInterval(() => {
      if (idx >= frames.length - 1) { stop(); return; }
      next();
    }, PLAY_MS);
  }

  btnPrev.addEventListener("click", () => { stop(); go(idx - 1); });
  btnNext.addEventListener("click", () => { stop(); next(); });
  btnReset.addEventListener("click", () => { stop(); go(0); });
  btnPlay.addEventListener("click", () => (timer ? stop() : play()));

  // Listen for the custom modechange event to trigger a re-render
  window.addEventListener("modechange", () => {
    render();
  });

  go(0);
})();
