# Interactive demo — Two-Channel Cascade

An in-browser, **illustrative** visualization of the two-channel cascade model:
bootstrap percolation (the *solvency* channel) plus a self-reinforcing global
*fear* field, on an Erdős–Rényi graph $G(n,p)$.

It animates a cascade round-by-round at small $n$ so you can see individual banks
fail and tell the two channels apart by color:

| color | meaning |
|---|---|
| gray | solvent |
| black | seed (initial shock at $t=0$) |
| orange | failed via **solvency** (≥ $r$ failed neighbors — the Janson channel) |
| purple | failed via **fear** (panic draw, prob. $f_i\,g_t$) |

The live panel tracks the round $t$, new failures $a_t$, failed fraction
$A(t)/n$, the systemic flag ($|A^*|/n \ge \theta{=}0.5$), and the **panic field**
$g_t = a_{t-1}/n$ as a thermometer — which spikes then decays, illustrating that
fear is a *subcritical amplifier* ($R_\text{fear}\approx\mu<1$), not an igniter.

Sliders: $r$ (solvency threshold), $\mu$ (mean fear), $\kappa$ (fear
heterogeneity), $a$ (seed size), $p$ (connectivity), $n$ (number of banks), plus a
seed field for reproducibility.

## ⚠️ This is NOT the validated engine

The cascade here runs in **JavaScript** (`cascade.js`) and is a *teaching*
reimplementation of the §3.4 dynamics. The project's source of truth is
`src/twocascade/reference.py` (the oracle); research results come from the C++
core cross-validated against it (§5.4). This demo:

- runs at small $n$ (≤150) — the **mechanism**, not the asymptotic/research regime
  ($n\ge1000$);
- is deliberately **not** cross-validated against the oracle;
- **must not** be cited as a result.

It does mirror the real model faithfully where it matters: simultaneous updates,
the incremental fear field $g_t=a_{t-1}/n$, and $f_i\sim\text{Beta}(\mu\kappa,(1-\mu)\kappa)$
so $E[f]=\mu$ (with the $\mu=0/\mu=1$ guards).

## Run it

Locally — just open `index.html`, or serve the folder:

```sh
cd viz && python3 -m http.server 8000   # then open http://localhost:8000
```

Online — GitHub Pages publishes this folder via
`.github/workflows/pages.yml`. The workflow auto-enables Pages
(`configure-pages` with `enablement: true`); if your org restricts that, set repo
**Settings → Pages → Source = GitHub Actions** once by hand. vis-network is
**vendored locally** (`vendor/`), so there is no CDN dependency and no build step —
the page works offline and from `file://` too.

## Files
- `index.html` — layout, sliders (with tooltips), legend, live panel.
- `cascade.js` — seeded RNG, Beta sampler, the §3.4 cascade engine, trace output.
- `app.js` — wires the engine to vis-network and the playback controls.
- `style.css` — styling.
- `vendor/vis-network.min.js` — vendored graph library (vis-network 9.1.9, no CDN).
