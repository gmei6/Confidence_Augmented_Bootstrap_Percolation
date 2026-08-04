/* TwoCascade interactive poster demo -- playback only.
 *
 * Nothing here simulates a cascade. Every animation replays a trace JSON dumped
 * by scripts/dump_poster_demo_traces.py from the Python reference engine, so the
 * page is deterministic and matches the committed configs and seeds.
 *
 * Trace schema: twocascade-poster-demo-trace/1
 *   nodes  [[x, y], ...]          fixed layout in [0, 1]^2, index = node id
 *   edges  [[u, v], ...]          undirected, u < v
 *   rounds [{round: 0, seed: []}, {round: t, structural: [], fear: []}, ...]
 */
'use strict';

/* ------------------------------------------------------------------ constants */
var COLORS = {
  healthy: '#2E6E76',      // teal
  structural: '#BD5A2E',   // rust
  fear: '#8E4A72',         // plum
  seed: '#E8834B',         // brighter rust: the initial shock
  // Edges have to READ as structure on a phone in daylight, so they are drawn
  // well above a hairline alpha. Three tiers, all still dimmer than the opaque
  // nodes: live links, links touching something that has already failed, and
  // (GIRG only) torus wrap-around links, which are real edges but cross the
  // whole panel and would otherwise dominate the picture.
  edge: 'rgba(190, 205, 222, 0.30)',
  edgeBurnt: 'rgba(189, 90, 46, 0.42)',
  edgeWrap: 'rgba(190, 205, 222, 0.11)'
};

var PRE_ROLL_MS = 900;   // hold on the initial shock before round 1
var STEP_MS = 720;       // fixed pace: one cascade round per this many ms
var POP_MS = 320;        // how long a newly failed node flares

// Node radius scales with degree, so the poster's actual story -- heavy-tailed
// hubs versus homogeneous ER -- is visible before anything fails. Sublinear and
// clamped: (deg / median deg) ^ 0.45, held inside [0.62, 3.0] of the base
// radius. Measured on the shipped traces, that gives ER a 0.62-1.64 spread
// (95th pct 1.37, reads as uniform) against power-law 0.73-3.00 (95th pct 2.07,
// two hubs at the cap) -- the contrast between families is the point, and the
// cap keeps the biggest hub from swallowing the screen.
var DEG_EXP = 0.45;
var DEG_MIN = 0.62;
var DEG_MAX = 3.0;

var ST = { HEALTHY: 0, SEED: 1, STRUCTURAL: 2, FEAR: 3 };

/* -------------------------------------------------------------------- phases */
var PHASES = [
  { kind: 'landing' },
  {
    kind: 'single', badge: 'Erdős–Rényi · fear 0 · two-bank shock',
    traces: ['traces/phase1_er_mu0.json']
  },
  {
    kind: 'single', badge: 'Same graph · fear 0.4',
    traces: ['traces/phase2_er_mu04.json'],
    measured: 'Measured, not asserted: over 400 graph seeds at this size, a ' +
      'two-bank shock never ignited with fear off, and ignited in 4 of 400 with ' +
      'fear on. At the poster’s n = 10,000 it ignites in 0 of 500 at every ' +
      'fear level — fear amplifies cascades the structure allows, it cannot ' +
      'start them alone.'
  },
  {
    kind: 'single', badge: 'Power-law hubs · fear 0',
    traces: ['traces/phase3_powerlaw_mu0.json']
  },
  {
    kind: 'single', badge: 'Same graph · fear 0.4',
    traces: ['traces/phase4_powerlaw_mu04.json']
  },
  {
    kind: 'single', badge: 'Same graph · fear 0.7',
    traces: ['traces/phase5_powerlaw_mu07.json'],
    measured: 'Phases 3–5 hold the graph and the two starting banks bit-for-bit ' +
      'identical — same seed, same layout. Only the fear level changes. What ' +
      'they show is fear accelerating and extending a cascade the structure was ' +
      'already going to sustain, not fear starting one; that is the next screen.'
  },
  {
    kind: 'stacked', badge: 'Power-law vs GIRG · both at fear 0.4',
    traces: ['traces/phase4_powerlaw_mu04.json', 'traces/phase6_girg_mu04.json'],
    labels: ['power-law — no geometry', 'GIRG — hubs on a map'],
    headline: 'Does geometry change the story?',
    caption: 'Top: the heavy-tailed network from the last three screens. Bottom: the ' +
      'same kind of hubs, but every bank now sits somewhere on a map and links ' +
      'prefer near neighbours — so the bottom panel is drawn at its real ' +
      'coordinates. Same fear, same average number of links (4.2 vs 4.1), same ' +
      'two-bank shock.',
    measured: 'Geometry changes what the burn looks like, not whether it burns: ' +
      '85% of the network down without geometry, 82% with. That matches the ' +
      'poster’s cross-family comparison, where the power-law and GIRG curves ' +
      'sit essentially on top of each other.'
  },
  {
    kind: 'chooser',
    traces: ['traces/phase7_trial1.json', 'traces/phase7_trial2.json',
             'traces/phase7_trial3.json'],
    cards: [
      { name: 'Run A', hint: 'scan order k = 0' },
      { name: 'Run B', hint: 'scan order k = 2' },
      { name: 'Run C', hint: 'scan order k = 24' }
    ],
    measured: 'Of 400 runs on this one network, 266 never got past the first bank, ' +
      '85 sputtered and died, and 42 took most of the system. Every one of those ' +
      '42 was started by fear — at fear 0 the structural rule cannot fire from ' +
      'a single failure, so the count would be exactly 0. The project’s ' +
      'measured population result, over freshly drawn networks at full size, is an ' +
      'ignition rate of about 1 − e^(−fear): roughly a third at fear 0.4. ' +
      'One small network is a single draw from that population, not the population.'
  }
];

/* -------------------------------------------------------------------- helpers */
function $(id) { return document.getElementById(id); }

var traceCache = {};
function loadTrace(path) {
  if (traceCache[path]) { return traceCache[path]; }
  traceCache[path] = fetch(path).then(function (r) {
    if (!r.ok) { throw new Error(path + ' -> HTTP ' + r.status); }
    return r.json();
  });
  return traceCache[path];
}

/* --------------------------------------------------------------------- player */
function Player(card, trace, label) {
  this.card = card;
  this.trace = trace;
  this.canvas = card.querySelector('canvas');
  this.ctx = this.canvas.getContext('2d');
  this.statEl = card.querySelector('.panel-stat');
  this.label = label;
  this.n = trace.params.n;
  this.maxRound = trace.rounds.length - 1;
  this.state = new Uint8Array(this.n);
  this.failedAt = new Int16Array(this.n).fill(-1);
  this.round = 0;
  this.counts = { failed: 0, structural: 0, fear: 0 };
  this.degScale = degreeScale(trace);
  this.wrapEdge = wrapEdgeFlags(trace);
  this.resize();
  this.reset();
}

/* Per-node radius multiplier from the trace's own edge list. */
function degreeScale(trace) {
  var n = trace.params.n, i;
  var deg = new Uint16Array(n);
  for (i = 0; i < trace.edges.length; i++) {
    deg[trace.edges[i][0]]++;
    deg[trace.edges[i][1]]++;
  }
  var sorted = Array.prototype.slice.call(deg).sort(function (a, b) { return a - b; });
  var median = Math.max(1, sorted[Math.floor(n / 2)]);
  var scale = new Float32Array(n);
  for (i = 0; i < n; i++) {
    scale[i] = Math.min(DEG_MAX, Math.max(DEG_MIN, Math.pow(deg[i] / median, DEG_EXP)));
  }
  return scale;
}

/* GIRG lives on a torus, so a link between x = 0.02 and x = 0.98 is a SHORT
 * link drawn across the whole panel. Flag those so they can be dimmed rather
 * than deleted -- they are real edges, and hiding them would misdraw the graph. */
function wrapEdgeFlags(trace) {
  var flags = new Uint8Array(trace.edges.length);
  if (!trace.layout || trace.layout.kind !== 'girg_positions') { return flags; }
  for (var i = 0; i < trace.edges.length; i++) {
    var a = trace.nodes[trace.edges[i][0]], b = trace.nodes[trace.edges[i][1]];
    if (Math.abs(a[0] - b[0]) > 0.5 || Math.abs(a[1] - b[1]) > 0.5) { flags[i] = 1; }
  }
  return flags;
}

Player.prototype.resize = function () {
  var dpr = window.devicePixelRatio || 1;
  var rect = this.canvas.getBoundingClientRect();
  var w = Math.max(1, Math.round(rect.width));
  var h = Math.max(1, Math.round(rect.height));
  this.canvas.width = Math.round(w * dpr);
  this.canvas.height = Math.round(h * dpr);
  this.dpr = dpr;
  this.W = this.canvas.width;
  this.H = this.canvas.height;
  // Base radius: the MEDIAN node. Hubs multiply up from here (see DEG_MAX), so
  // this is deliberately smaller than a one-size-fits-all radius would be --
  // otherwise the top hubs overlap their neighbours at n = 300.
  this.r = Math.max(2.2, Math.min(4.6, Math.min(w, h) / 115)) * dpr;
  this.pad = this.r * DEG_MAX * 1.6;
};

Player.prototype.reset = function () {
  this.state.fill(ST.HEALTHY);
  this.failedAt.fill(-1);
  this.round = 0;
  this.counts = { failed: 0, structural: 0, fear: 0 };
  this.applyRound(0);
  this.roundStart = performance.now();
};

Player.prototype.applyRound = function (k) {
  var rd = this.trace.rounds[k], i;
  if (!rd) { return; }
  if (rd.seed) {
    for (i = 0; i < rd.seed.length; i++) {
      this.state[rd.seed[i]] = ST.SEED;
      this.failedAt[rd.seed[i]] = k;
      this.counts.failed++;
    }
  }
  if (rd.structural) {
    for (i = 0; i < rd.structural.length; i++) {
      this.state[rd.structural[i]] = ST.STRUCTURAL;
      this.failedAt[rd.structural[i]] = k;
      this.counts.failed++; this.counts.structural++;
    }
  }
  if (rd.fear) {
    for (i = 0; i < rd.fear.length; i++) {
      this.state[rd.fear[i]] = ST.FEAR;
      this.failedAt[rd.fear[i]] = k;
      this.counts.failed++; this.counts.fear++;
    }
  }
};

Player.prototype.advance = function (now) {
  if (this.round >= this.maxRound) { return false; }
  this.round++;
  this.applyRound(this.round);
  this.roundStart = now;
  return true;
};

Player.prototype.done = function () { return this.round >= this.maxRound; };

Player.prototype.draw = function (now, cb) {
  var ctx = this.ctx, t = this.trace, i;
  var W = this.W, H = this.H, pad = this.pad, r = this.r;
  var sx = W - 2 * pad, sy = H - 2 * pad;
  ctx.clearRect(0, 0, W, H);

  // ---- edges: three batched passes, drawn under the nodes ---------------- //
  // pass 0 = torus wrap-arounds (GIRG only, dimmed), 1 = live links,
  // 2 = links touching a failed node. Batching keeps this to three paths a
  // frame regardless of edge count.
  var tiers = [
    { style: COLORS.edgeWrap, w: 0.55 },
    { style: COLORS.edge, w: 0.75 },
    { style: COLORS.edgeBurnt, w: 0.85 }
  ];
  for (var tier = 0; tier < 3; tier++) {
    ctx.strokeStyle = tiers[tier].style;
    ctx.lineWidth = Math.max(0.6, tiers[tier].w * this.dpr);
    ctx.beginPath();
    var drew = false;
    for (i = 0; i < t.edges.length; i++) {
      var u = t.edges[i][0], v = t.edges[i][1];
      var mine = this.wrapEdge[i] ? 0
        : (this.state[u] !== ST.HEALTHY || this.state[v] !== ST.HEALTHY) ? 2 : 1;
      if (mine !== tier) { continue; }
      var a = t.nodes[u], b = t.nodes[v];
      ctx.moveTo(pad + a[0] * sx, pad + a[1] * sy);
      ctx.lineTo(pad + b[0] * sx, pad + b[1] * sy);
      drew = true;
    }
    if (drew) { ctx.stroke(); }
  }

  // ---- nodes -------------------------------------------------------------- //
  var pop = Math.min(1, (now - this.roundStart) / POP_MS);
  for (i = 0; i < this.n; i++) {
    var p = t.nodes[i];
    var x = pad + p[0] * sx, y = pad + p[1] * sy;
    var st = this.state[i];
    var fresh = this.failedAt[i] === this.round && pop < 1;
    var rad = r * this.degScale[i] * (st === ST.HEALTHY ? 0.88 : 1.0) *
              (fresh ? 1 + 1.1 * (1 - pop) : 1);
    var col = st === ST.HEALTHY ? COLORS.healthy
            : st === ST.SEED ? COLORS.seed
            : st === ST.STRUCTURAL ? COLORS.structural : COLORS.fear;

    if (fresh) {                                  // flare ring on the round it fails
      ctx.globalAlpha = 0.45 * (1 - pop);
      ctx.beginPath();
      ctx.arc(x, y, rad * 2.4, 0, Math.PI * 2);
      ctx.fillStyle = col;
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    ctx.fillStyle = col;
    ctx.beginPath();
    if (!cb || st === ST.HEALTHY) {
      ctx.arc(x, y, rad, 0, Math.PI * 2);
    } else if (st === ST.FEAR) {                  // colour-blind mode: triangle
      var h = rad * 1.35;
      ctx.moveTo(x, y - h);
      ctx.lineTo(x + h * 0.95, y + h * 0.72);
      ctx.lineTo(x - h * 0.95, y + h * 0.72);
      ctx.closePath();
    } else {                                      // colour-blind mode: square
      var s = rad * 1.1;
      ctx.rect(x - s, y - s, 2 * s, 2 * s);
    }
    ctx.fill();

    if (st === ST.SEED) {                         // the initial shock keeps a ring
      ctx.strokeStyle = 'rgba(255,255,255,0.85)';
      ctx.lineWidth = Math.max(1, 1.1 * this.dpr);
      ctx.beginPath();
      ctx.arc(x, y, rad * 1.75, 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  if (this.statEl) {
    this.statEl.textContent = Math.round(100 * this.counts.failed / this.n) + '% down';
  }
};

/* ---------------------------------------------------------------- controller */
var app = {
  phase: 0,
  trial: null,
  players: [],
  playing: false,
  lastStep: 0,
  cb: false
};

function makeCard(label, withStat) {
  var card = document.createElement('div');
  card.className = 'canvas-card';
  card.innerHTML = '<canvas></canvas>' +
    (label ? '<div class="panel-label">' + label + '</div>' : '') +
    (withStat ? '<div class="panel-stat"></div>' : '');
  return card;
}

function sizeCards(stacked) {
  var wrap = $('canvasWrap');
  var w = wrap.clientWidth || 320;
  var vh = window.innerHeight;
  var cards = wrap.querySelectorAll('.canvas-card');
  var h = stacked
    ? Math.max(150, Math.min(w * 0.78, (vh - 330) / 2))
    : Math.max(200, Math.min(w, vh * 0.52));
  for (var i = 0; i < cards.length; i++) { cards[i].style.height = h + 'px'; }
}

function showScreen(id) {
  ['screen-landing', 'screen-demo', 'screen-chooser'].forEach(function (s) {
    $(s).classList.toggle('active', s === id);
  });
}

function renderDots() {
  var dots = $('dots');
  if (!dots.childElementCount) {
    for (var i = 0; i < PHASES.length; i++) {
      var b = document.createElement('button');
      b.className = 'dot';
      b.setAttribute('aria-label', 'Screen ' + i);
      b.dataset.i = String(i);
      b.addEventListener('click', function (e) { goto(+e.currentTarget.dataset.i); });
      dots.appendChild(b);
    }
  }
  var kids = dots.children;
  for (var j = 0; j < kids.length; j++) {
    kids[j].classList.toggle('current', j === app.phase);
    kids[j].classList.toggle('seen', j < app.phase);
  }
}

function updateNav() {
  var back = $('backBtn'), next = $('nextBtn');
  back.disabled = app.phase === 0 && app.trial === null;
  if (app.phase === 0) {
    next.textContent = 'Begin →';
  } else if (app.trial !== null) {
    next.textContent = 'Pick another →';
  } else if (app.phase === PHASES.length - 1) {
    next.textContent = 'Poster notes →';
  } else {
    next.textContent = 'Next →';
  }
}

function showError(msg) {
  var wrap = $('canvasWrap');
  wrap.innerHTML = '<div class="error"><strong>Could not load the cascade traces.</strong><br>' +
    msg + '<br><br>If you opened this file directly from disk, the browser blocks ' +
    'reading the trace JSONs. Serve the folder instead: ' +
    '<code>python3 -m http.server</code> from <code>poster-demo/</code>.</div>';
}

function goto(i) {
  if (i < 0 || i >= PHASES.length) { return; }
  app.phase = i;
  app.trial = null;
  app.players = [];
  app.playing = false;
  renderDots();
  updateNav();
  var ph = PHASES[i];

  if (ph.kind === 'landing') { showScreen('screen-landing'); return; }
  if (ph.kind === 'chooser') { showScreen('screen-chooser'); renderChooser(ph); return; }
  showScreen('screen-demo');
  mountTraces(ph, ph.traces, ph.kind === 'stacked');
}

var chooserReady = false;
function renderChooser(ph) {
  var box = $('trialCards');
  if (chooserReady) { return; }
  Promise.all(ph.traces.map(loadTrace)).then(function (traces) {
    box.innerHTML = '';
    chooserReady = true;
    traces.forEach(function (tr, idx) {
      var meta = ph.cards[idx];
      var btn = document.createElement('button');
      btn.className = 'trial-card';
      btn.innerHTML = '<div class="t-name">' + meta.name + '</div>' +
        '<div class="t-sub">Seed bank #' + tr.rounds[0].seed[0] +
        ' · trial seed ' + tr.seeds.trial + '</div>' +
        '<div class="t-hint">' + meta.hint + ' · outcome hidden until you play it</div>';
      btn.addEventListener('click', function () { playTrial(idx); });
      box.appendChild(btn);
    });
  }).catch(function (e) {
    box.innerHTML = '<div class="error">Could not load the trial traces: ' + e.message +
      '. Serve this folder over HTTP (<code>python3 -m http.server</code>).</div>';
  });
}

function playTrial(idx) {
  var ph = PHASES[PHASES.length - 1];
  app.trial = idx;
  showScreen('screen-demo');
  $('backToTrials').hidden = false;
  mountTraces(ph, [ph.traces[idx]], false, ph.cards[idx].name);
  updateNav();
}

var mountSeq = 0;

function mountTraces(ph, paths, stacked, trialName) {
  var wrap = $('canvasWrap');
  wrap.innerHTML = '';
  $('backToTrials').hidden = app.trial === null;
  $('badge').textContent = ph.badge || 'Power-law · one failed bank · fear 0.4';
  $('headline').textContent = 'Loading…';
  $('readout').textContent = '';
  $('progressFill').style.width = '0%';       // don't leave the last phase's bar full
  $('progress').classList.remove('done');
  $('caption').textContent = '';
  $('measured').hidden = true;

  var mySeq = ++mountSeq;
  Promise.all(paths.map(loadTrace)).then(function (traces) {
    if (mySeq !== mountSeq) { return; }   // a later navigation won the race
    var head = ph.headline || traces[0].text.headline;
    $('headline').textContent = trialName ? trialName + ' — ' + head : head;
    $('caption').textContent = ph.caption || traces[0].text.caption;
    if (ph.measured) { $('measured').textContent = ph.measured; $('measured').hidden = false; }

    app.players = traces.map(function (tr, i) {
      var card = makeCard(stacked ? ph.labels[i] : null, stacked);
      wrap.appendChild(card);
      return { card: card, trace: tr };
    });
    sizeCards(stacked);
    app.players = app.players.map(function (o, i) {
      return new Player(o.card, o.trace, stacked ? ph.labels[i] : null);
    });
    startPlayback();
  }).catch(function (e) {
    if (mySeq === mountSeq) { showError(e.message); }
  });
}

function startPlayback() {
  app.players.forEach(function (p) { p.reset(); });
  app.playing = true;
  app.lastStep = performance.now() + (PRE_ROLL_MS - STEP_MS);
  updateReadout();
}

/* One bar per screen. Phase 6's two canvases share a clock, so they share this
 * bar; it tracks the longer of the two cascades. */
function updateProgress(curR, maxR, allDone) {
  var pct = allDone || maxR <= 0 ? 100 : Math.round(100 * curR / maxR);
  $('progressFill').style.width = pct + '%';
  $('progress').setAttribute('aria-valuenow', String(pct));
  $('progress').classList.toggle('done', pct >= 100);
}

function updateReadout() {
  if (!app.players.length) { return; }
  var p = app.players[0];
  var allDone = app.players.every(function (q) { return q.done(); });
  var maxR = Math.max.apply(null, app.players.map(function (q) { return q.maxRound; }));
  var curR = Math.max.apply(null, app.players.map(function (q) { return q.round; }));
  updateProgress(curR, maxR, allDone);
  var parts = [];
  if (app.players.length === 1) {
    parts.push('<b>' + p.counts.failed + '</b> of ' + p.n + ' down');
    parts.push('<span class="struct-n">' + p.counts.structural + ' by neighbours</span>');
    parts.push('<span class="fear-n">' + p.counts.fear + ' by fear</span>');
  } else {
    app.players.forEach(function (q, i) {
      parts.push((i === 0 ? 'top' : 'bottom') + ': <b>' + q.counts.failed + '</b>/' + q.n +
        ' <span class="fear-n">(' + q.counts.fear + ' by fear)</span>');
    });
  }
  if (allDone) { parts.push('cascade finished'); }
  $('readout').innerHTML = parts.join(' · ');
}

function frame(now) {
  if (app.players.length) {
    if (app.playing && now - app.lastStep >= STEP_MS) {
      app.lastStep = now;
      var moved = false;
      app.players.forEach(function (p) { moved = p.advance(now) || moved; });
      if (!moved) { app.playing = false; }
      updateReadout();
    }
    app.players.forEach(function (p) { p.draw(now, app.cb); });
  }
  requestAnimationFrame(frame);
}

/* ------------------------------------------------------------------- wiring */
function next() {
  if (app.trial !== null) { goto(PHASES.length - 1); return; }
  if (app.phase === PHASES.length - 1) { $('notesOverlay').classList.add('open'); return; }
  goto(app.phase + 1);
}
function back() {
  if (app.trial !== null) { goto(PHASES.length - 1); return; }
  goto(app.phase - 1);
}

$('nextBtn').addEventListener('click', next);
$('backBtn').addEventListener('click', back);
$('beginBtn').addEventListener('click', function () { goto(1); });
$('replayBtn').addEventListener('click', function () {
  if (app.players.length) { startPlayback(); }
});
$('backToTrials').addEventListener('click', function () { goto(PHASES.length - 1); });
$('notesBtn').addEventListener('click', function () { $('notesOverlay').classList.add('open'); });
$('closeNotes').addEventListener('click', function () { $('notesOverlay').classList.remove('open'); });

$('cbToggle').addEventListener('click', function () {
  app.cb = !app.cb;
  document.body.classList.toggle('cb', app.cb);
  this.setAttribute('aria-pressed', app.cb ? 'true' : 'false');
  this.textContent = app.cb ? 'shapes on' : 'shapes';
  try { localStorage.setItem('tc_cb', app.cb ? '1' : '0'); } catch (e) { /* private mode */ }
});

document.addEventListener('keydown', function (e) {
  if ($('notesOverlay').classList.contains('open')) {
    if (e.key === 'Escape') { $('notesOverlay').classList.remove('open'); }
    return;
  }
  if (e.key === 'ArrowRight') { next(); }
  if (e.key === 'ArrowLeft') { back(); }
  if (e.key === 'r' && app.players.length) { startPlayback(); }
});

var resizeTimer = null;
window.addEventListener('resize', function () {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function () {
    if (!app.players.length) { return; }
    sizeCards(app.players.length > 1);
    app.players.forEach(function (p) { p.resize(); });
  }, 120);
});

(function init() {
  try {
    if (localStorage.getItem('tc_cb') === '1') { $('cbToggle').click(); }
  } catch (e) { /* private mode */ }
  renderDots();
  updateNav();
  loadTrace(PHASES[1].traces[0]);   // warm the first trace while the landing shows
  requestAnimationFrame(frame);
})();
