import os
from bs4 import BeautifulSoup

os.makedirs(".lavish", exist_ok=True)

with open("advisor-update-2026-07-22/index.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Get the CSS and head
head = soup.head

# Get the section
rgg_section = soup.find(id="group-rgg")

cards = rgg_section.find_all("div", class_="card")

# Insert placeholders
placeholder1_html = """
<figure class="diagram-figure">
  <div class="diagram-placeholder">
    <span class="dp-tag">Chart / Graph</span>
    <span class="dp-desc">Line chart comparing global vs local vs control slope. X-axis: n, Y-axis: time/ratio.</span>
  </div>
  <figcaption>Panic that spreads globally speeds up collapse; panic that only spreads locally doesn't change the pace.</figcaption>
</figure>
"""

placeholder2_html = """
<figure class="diagram-figure">
  <div class="diagram-placeholder">
    <span class="dp-tag">Chart</span>
    <span class="dp-desc">Wider grid chart showing global field log-ratio vs log-n. It shows the slope steepening/not flattening compared to control.</span>
  </div>
  <figcaption>Global fear outrunning the collapse front as a stable power law at large n.</figcaption>
</figure>
"""

placeholder3_html = """
<figure class="diagram-figure">
  <div class="diagram-placeholder">
    <span class="dp-tag">Diagram</span>
    <span class="dp-desc">Diagram showing why cross-round clusters never form due to r_n exclusion, contrasting real process vs null model.</span>
  </div>
  <figcaption>Structural tautology: real remote points can't be closer than r_n by definition, while null points can.</figcaption>
</figure>
"""

placeholders = [placeholder1_html, placeholder2_html, placeholder3_html]

for i, card in enumerate(cards):
    details_body = card.find("div", class_="details-body")
    if details_body and i < len(placeholders):
        p_soup = BeautifulSoup(placeholders[i], "html.parser")
        details_body.append(p_soup)

# Create final HTML
final_soup = BeautifulSoup("<!DOCTYPE html><html><body><div class='layout'><main></main></div></body></html>", "html.parser")
final_soup.html.insert(0, head)
final_soup.main.append(rgg_section)

with open(".lavish/geometric.html", "w", encoding="utf-8") as f:
    f.write(str(final_soup))

print("Created .lavish/geometric.html")
