def y(val): return 180 - (val - 0.2)/0.5 * 140
xs = [100, 260, 420, 580]
ns = ["4k", "8k", "16k", "32k"]

control = [0.685, 0.682, 0.676, 0.669]
local2 = [0.686, 0.679, 0.674, 0.666]
local4 = [0.678, 0.680, 0.675, 0.667]
global2 = [0.461, 0.393, 0.325, 0.273]
global4 = [0.389, 0.325, 0.270, 0.219]

def path(data):
    return "M " + " L ".join([f"{x},{y(v):.1f}" for x, v in zip(xs, data)])

def points(data):
    return "\n".join([f'<circle cx="{x}" cy="{y(v):.1f}" r="4" class="dg-dot" />' for x, v in zip(xs, data)])

svg1 = f'''
<svg class="impl-svg" viewBox="0 0 700 230" role="img" aria-label="Line chart comparing collapse times">
  <!-- Axes -->
  <line x1="50" y1="20" x2="50" y2="180" class="dg-axis" />
  <line x1="50" y1="180" x2="650" y2="180" class="dg-axis" />
  <text x="40" y="30" text-anchor="end" class="dg-sub">0.7</text>
  <text x="40" y="185" text-anchor="end" class="dg-sub">0.2</text>
  
  <!-- X labels -->
  {"".join([f'<text x="{x}" y="200" text-anchor="middle" class="dg-sub">n={n}</text>' for x, n in zip(xs, ns)])}
  
  <!-- Control / Local (Bundle) -->
  <path d="{path(control)}" stroke="var(--ink-soft)" stroke-width="2" fill="none" />
  <path d="{path(local2)}" stroke="var(--ink-soft)" stroke-width="2" fill="none" stroke-dasharray="4 2" />
  <path d="{path(local4)}" stroke="var(--ink-soft)" stroke-width="2" fill="none" stroke-dasharray="2 2" />
  <text x="600" y="{y(0.669) - 10:.1f}" class="dg-sub" fill="var(--ink-soft)">Control &amp; Local (flat)</text>
  
  <!-- Global 0.2 -->
  <path d="{path(global2)}" stroke="var(--accent-warm)" stroke-width="2.5" fill="none" />
  <text x="600" y="{y(0.273) - 5:.1f}" class="dg-sub" fill="var(--accent-warm)">Global μ̄=0.2</text>
  
  <!-- Global 0.4 -->
  <path d="{path(global4)}" stroke="var(--bad)" stroke-width="2.5" fill="none" />
  <text x="600" y="{y(0.219) + 15:.1f}" class="dg-sub" fill="var(--bad)">Global μ̄=0.4</text>
</svg>
'''

# Diagram 2: Conceptual line chart vs Spatial representation
# Let's do a spatial representation showing "Local vs Global" propagation
svg2 = '''
<svg class="impl-svg" viewBox="0 0 700 230" role="img" aria-label="Local fear rides front, global fear outruns it">
  <defs>
    <radialGradient id="frontGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="var(--bad)" stop-opacity="0.3" />
      <stop offset="100%" stop-color="var(--bad)" stop-opacity="0" />
    </radialGradient>
  </defs>
  
  <!-- Left Panel: Local Fear -->
  <g transform="translate(0,0)">
    <text x="175" y="25" text-anchor="middle" class="dg-title">Local Fear: Rides the Front</text>
    <rect x="50" y="50" width="250" height="150" class="dg-edge" />
    <!-- Collapse front -->
    <circle cx="175" cy="125" r="50" fill="url(#frontGrad)" />
    <circle cx="175" cy="125" r="50" fill="none" stroke="var(--bad)" stroke-width="1.5" stroke-dasharray="4 2" />
    <text x="175" y="125" text-anchor="middle" class="dg-sub">Collapse</text>
    
    <!-- Fear only just outside -->
    <circle cx="175" cy="125" r="65" fill="none" stroke="var(--accent-warm)" stroke-width="1.5" />
    <text x="175" y="60" text-anchor="middle" class="dg-sub" fill="var(--accent-warm)">Fear zone</text>
  </g>
  
  <!-- Right Panel: Global Fear -->
  <g transform="translate(350,0)">
    <text x="175" y="25" text-anchor="middle" class="dg-title">Global Fear: Outruns the Front</text>
    <rect x="50" y="50" width="250" height="150" class="dg-edge" />
    <!-- Collapse front -->
    <circle cx="175" cy="125" r="30" fill="url(#frontGrad)" />
    <circle cx="175" cy="125" r="30" fill="none" stroke="var(--bad)" stroke-width="1.5" stroke-dasharray="4 2" />
    <text x="175" y="125" text-anchor="middle" class="dg-sub">Main front</text>
    
    <!-- New outbreak ahead -->
    <circle cx="250" cy="80" r="15" fill="url(#frontGrad)" />
    <circle cx="250" cy="80" r="15" fill="none" stroke="var(--bad)" stroke-width="1.5" stroke-dasharray="4 2" />
    <text x="250" y="60" text-anchor="middle" class="dg-sub">New outbreak</text>
    
    <circle cx="90" cy="160" r="10" fill="url(#frontGrad)" />
    <circle cx="90" cy="160" r="10" fill="none" stroke="var(--bad)" stroke-width="1.5" stroke-dasharray="4 2" />
    
    <!-- Fear field is everywhere -->
    <rect x="50" y="50" width="250" height="150" fill="var(--accent-warm)" fill-opacity="0.1" />
  </g>
</svg>
'''

# Diagram 3: Exclusion Zone Tautology
svg3 = '''
<svg class="impl-svg" viewBox="0 0 700 230" role="img" aria-label="Diagram showing why cross-round clusters never form due to exclusion zone">
  <defs>
    <radialGradient id="exclusionGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="var(--accent-cool)" stop-opacity="0.2" />
      <stop offset="100%" stop-color="var(--accent-cool)" stop-opacity="0" />
    </radialGradient>
  </defs>
  
  <g transform="translate(100, 0)">
    <text x="250" y="25" text-anchor="middle" class="dg-title">Measurement Tautology: The r_n Exclusion Zone</text>
    
    <!-- Round 1 Failure -->
    <circle cx="150" cy="125" r="8" fill="var(--bad)" />
    <text x="150" y="145" text-anchor="middle" class="dg-sub">Round 1 failed node</text>
    
    <!-- Exclusion Zone -->
    <circle cx="150" cy="125" r="80" fill="url(#exclusionGrad)" />
    <circle cx="150" cy="125" r="80" fill="none" stroke="var(--accent-cool)" stroke-width="1.5" stroke-dasharray="5 3" />
    <text x="150" y="55" text-anchor="middle" class="dg-sub" fill="var(--accent-cool)">Exclusion zone (r_n)</text>
    
    <!-- Null model point (allowed inside) -->
    <circle cx="200" cy="100" r="8" fill="var(--ink-soft)" />
    <text x="200" y="85" text-anchor="middle" class="dg-sub">Null point</text>
    <path d="M 195 105 L 155 120" stroke="var(--ink-soft)" stroke-width="1.5" stroke-dasharray="2 2" />
    <text x="160" y="105" class="dg-sub" fill="var(--ink-soft)">&lt; r_n (cluster!)</text>
    
    <!-- Real model point (pushed outside) -->
    <circle cx="280" cy="125" r="8" fill="var(--accent-warm)" />
    <text x="280" y="145" text-anchor="middle" class="dg-sub">Round 2 remote node</text>
    <path d="M 270 125 L 230 125" stroke="var(--accent-warm)" stroke-width="1.5" />
    <text x="235" y="120" class="dg-sub" fill="var(--accent-warm)">&gt; r_n</text>
    
    <text x="450" y="100" class="dg-sub" width="150">
      <tspan x="400" dy="0">By definition, a Round 2</tspan>
      <tspan x="400" dy="20">outbreak is only "remote"</tspan>
      <tspan x="400" dy="20">if it's > r_n from Round 1.</tspan>
      <tspan x="400" dy="30">But a "cluster" requires</tspan>
      <tspan x="400" dy="20">points to be < r_n apart.</tspan>
      <tspan x="400" dy="30" font-weight="bold" fill="var(--bad)">Real process count = 0</tspan>
    </text>
  </g>
</svg>
'''

with open(".lavish/geometric.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# We placed placeholders with <figure class="diagram-figure"> ... </figure>
# Let's replace the first, second, third occurrences.

figures = re.split(r'<figure class="diagram-figure">.*?</figure>', html, flags=re.DOTALL)
if len(figures) == 4:
    new_html = figures[0] + f'<figure class="diagram-figure">{svg1}</figure>' + figures[1] + f'<figure class="diagram-figure">{svg2}</figure>' + figures[2] + f'<figure class="diagram-figure">{svg3}</figure>' + figures[3]
    with open(".lavish/geometric.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Injected SVGs successfully.")
else:
    print("Found", len(figures), "figures, expected 4 parts.")

