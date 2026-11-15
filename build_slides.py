#!/usr/bin/env python3
"""Build slides.html — a 6-slide demo deck for the NASA Space Apps submission.
Reads the GISTEMP CSVs and embeds an SVG curve with gold dots on the 33
flagged months, plus the 60-second audio. Standard library only."""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "gistemp_monthly.csv"), newline="", encoding="utf-8") as f:
    rows = [(r["date"], float(r["value"])) for r in csv.DictReader(f)]
with open(os.path.join(HERE, "gistemp_events.csv"), newline="", encoding="utf-8") as f:
    flagged = {r["date"] for r in csv.DictReader(f) if r["surprise"] == "YES"}

values = [v for _, v in rows]
vmin, vmax = min(values), max(values)
W, H, PAD = 920, 300, 30

def xy(i, v):
    x = PAD + i * (W - 2 * PAD) / max(1, len(rows) - 1)
    y = H - PAD - (v - vmin) / (vmax - vmin) * (H - 2 * PAD)
    return x, y

pts = " ".join(f"{xy(i, v)[0]:.1f},{xy(i, v)[1]:.1f}" for i, (_, v) in enumerate(rows))
dots = "".join(
    f'<circle cx="{xy(i, v)[0]:.1f}" cy="{xy(i, v)[1]:.1f}" r="4.5" fill="#E8B923" stroke="#0D1B2A" stroke-width="1"/>'
    for i, (d, v) in enumerate(rows) if d in flagged
)
svg = (
    f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Global temperature anomaly, Jan 1999 to Oct 2026">'
    f'<rect width="{W}" height="{H}" fill="#0D1B2A"/>'
    f'<polyline points="{pts}" fill="none" stroke="#7FB3D5" stroke-width="2"/>'
    f"{dots}"
    f'<text x="{PAD}" y="20" fill="#F5F4F0" font-size="14">Global temperature anomaly (°C vs 1951–1980) — gold dots: 33 surprise months</text>'
    f'<text x="{PAD}" y="{H - 6}" fill="#9AB0C0" font-size="12">Jan 1999</text>'
    f'<text x="{W - PAD - 70}" y="{H - 6}" fill="#9AB0C0" font-size="12">Oct 2026 (+1.55 °C)</text>'
    "</svg>"
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hear the Warming — Demo Slides</title>
<style>
  body {{ margin: 0; background: #0D1B2A; color: #F5F4F0; font-family: Georgia, serif; }}
  .slide {{ min-height: 100vh; display: flex; flex-direction: column; justify-content: center; padding: 6vh 8vw; box-sizing: border-box; border-bottom: 1px solid #24344A; }}
  h1 {{ font-size: 2.6em; margin: 0 0 0.3em; }}
  h2 {{ font-size: 2em; margin: 0 0 0.4em; color: #E8B923; }}
  p, li {{ font-size: 1.35em; line-height: 1.55; max-width: 900px; }}
  .sub {{ color: #9AB0C0; font-size: 1.2em; }}
  .num {{ color: #5A7186; font-size: 1em; margin-top: 2em; }}
  a {{ color: #7FB3D5; }}
  audio {{ width: 100%; max-width: 640px; margin-top: 1em; }}
  .small {{ font-size: 1em; color: #9AB0C0; }}
</style>
</head>
<body>
<section class="slide">
  <h1>Hear the Warming</h1>
  <p class="sub">27 Years of Global Temperature in 60 Seconds</p>
  <p>NASA Space Apps Challenge 2026 · Windsor · Team Volgat — Mike Amega</p>
  <audio controls src="gistemp_jukebox.wav"></audio>
  <p class="small">Press play: 334 notes, one per month, January 1999 to October 2026.</p>
  <p class="num">1 / 6</p>
</section>
<section class="slide">
  <h2>The idea</h2>
  <p>One note per month. A higher temperature anomaly plays a higher pitch. In 60 seconds you hear the planet warming — no chart to read.</p>
  <p>334 months · January 1999 – October 2026 · NASA GISTEMP v4</p>
  <p class="num">2 / 6</p>
</section>
<section class="slide">
  <h2>How it works</h2>
  <ul>
    <li>Data: NASA GISTEMP v4, global land-ocean temperature index, monthly anomaly vs the 1951–1980 baseline.</li>
    <li>Surprise: a rolling z-score (25-month window, threshold z ≥ 2.0) flags 33 months out of 334. Flagged months play louder, with a brighter note (a fifth above).</li>
    <li>Built with plain Python, standard library only. No proprietary code, no third-party model.</li>
  </ul>
  <p class="num">3 / 6</p>
</section>
<section class="slide">
  <h2>What we heard</h2>
  {svg}
  <ul>
    <li>El Niño 2015–16: October 2015 – March 2016, up to +1.36 °C (Feb 2016).</li>
    <li>Record heat 2023: March and July–November 2023, including +1.48 °C (Sep 2023).</li>
    <li>October 2026: +1.55 °C — the hottest month in the entire series.</li>
  </ul>
  <p class="num">4 / 6</p>
</section>
<section class="slide">
  <h2>Why it matters — and the honest limits</h2>
  <p>27 years of warming is a slow curve that eyes glaze over. Hearing it makes the change immediate, and it works for people who cannot read a chart.</p>
  <p>Limits: the detector flags deviations in either direction, so it also catches cold dips (Jan 2008, Dec 2010, Feb 2021). The pitch scale is a listening choice, not a physical scale.</p>
  <p class="num">5 / 6</p>
</section>
<section class="slide">
  <h2>Links</h2>
  <p>Demo (audio + curve + moments):<br><a href="https://volgat.github.io/nasa-jukebox-2026/">https://volgat.github.io/nasa-jukebox-2026/</a></p>
  <p>Code, data and audio (open source, Apache 2.0):<br><a href="https://github.com/Volgat/nasa-jukebox-2026">https://github.com/Volgat/nasa-jukebox-2026</a></p>
  <p class="small">Note: the code and text of this project were written with the assistance of an AI coding assistant (Muse). The audio and the chart are computed deterministically from the NASA data, not AI-generated.</p>
  <p class="num">6 / 6</p>
</section>
</body>
</html>
"""

out = os.path.join(HERE, "slides.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("slides.html écrit:", len(html), "caractères,", len(rows), "mois,", len(flagged), "points dorés")
