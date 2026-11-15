#!/usr/bin/env python3
"""Build a single self-contained demo page for the NASA Jukebox/GISTEMP project.

Reads gistemp_monthly.csv and gistemp_events.csv, writes index.html next to
gistemp_jukebox.wav (referenced relatively). No external dependencies.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    months = []
    with open(os.path.join(HERE, "gistemp_monthly.csv")) as f:
        for row in csv.DictReader(f):
            months.append({"date": row["date"][:7], "value": float(row["value"])})
    surprise = set()
    with open(os.path.join(HERE, "gistemp_events.csv")) as f:
        for row in csv.DictReader(f):
            if row["surprise"]:
                surprise.add(row["date"][:7])
    return months, surprise


def main():
    months, surprise = load()
    values = [m["value"] for m in months]
    labels = [m["date"] for m in months]
    flags = [1 if m["date"] in surprise else 0 for m in months]
    clusters = [
        ("Late 2001 – early 2002", "Nov 2001 – Mar 2002, up to +0.88 °C"),
        ("January 2007", "+1.01 °C"),
        ("March 2010", "+0.92 °C"),
        ("El Niño 2015–16", "Oct 2015 – Mar 2016, up to +1.36 °C (Feb 2016)"),
        ("2019 – early 2020", "Mar 2019 – Feb 2020, up to +1.23 °C"),
        ("Record heat 2023", "Mar and Jul–Nov 2023, incl. +1.48 °C (Sep 2023)"),
        ("2026", "Aug +1.42 °C, Oct +1.55 °C — highest in the series"),
    ]
    data_json = json.dumps({"labels": labels, "values": values, "flags": flags})
    cluster_html = "\n".join(
        f'      <li><strong>{name}:</strong> {desc}</li>' for name, desc in clusters
    )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hear the Warming — 27 Years of Global Temperature in 60 Seconds</title>
<style>
  body {{ font-family: Georgia, serif; max-width: 760px; margin: 2em auto; padding: 0 1em; color: #1a1a1a; line-height: 1.5; }}
  h1 {{ font-size: 1.6em; }} h2 {{ font-size: 1.2em; margin-top: 1.5em; }}
  audio {{ width: 100%; margin: 1em 0; }}
  canvas {{ width: 100%; height: 260px; border: 1px solid #ccc; }}
  .note {{ color: #555; font-size: 0.95em; }}
  li {{ margin-bottom: 0.3em; }}
</style>
</head>
<body>
<h1>Hear the Warming — 27 Years of Global Temperature in 60 Seconds</h1>
<p>NASA Space Apps Challenge 2026 — The Earth Information Jukebox. One note per
month, January 1999 to October 2026. Higher anomaly, higher pitch. Months that
stand out from their 25-month neighbourhood play louder.</p>
<audio controls src="gistemp_jukebox.wav"></audio>
<canvas id="chart" width="760" height="260"></canvas>
<p class="note">Gold dots: the 33 "surprise" months (rolling z-score &ge; 2.0, 25-month window).
Data: NASA GISTEMP v4, global land-ocean monthly anomaly vs 1951&ndash;1980, in &deg;C.
Source: <a href="https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv">GLB.Ts+dSST.csv</a>.</p>
<h2>What you hear</h2>
<ul>
{cluster_html}
</ul>
<h2>Honest limits</h2>
<p>The detector flags deviations in either direction, so it also catches cold dips
(Jan 2008, Dec 2010, Feb 2021). Because the series trends upward, a rolling z-score
flags many recent points; 33 moments is too many to narrate one by one, so the
clusters above are named instead. The pitch scale is a listening choice, not a
physical scale.</p>
<p class="note">Method: plain Python, standard library only, rolling z-score.
No proprietary code. Code, data and audio are open source (Apache 2.0).</p>
<script>
const D = {data_json};
const c = document.getElementById('chart'), x = c.getContext('2d');
const W = c.width, H = c.height, pad = 28;
const min = Math.min(...D.values), max = Math.max(...D.values);
const X = i => pad + i * (W - 2 * pad) / (D.values.length - 1);
const Y = v => H - pad - (v - min) * (H - 2 * pad) / (max - min);
x.strokeStyle = '#999'; x.beginPath(); x.moveTo(pad, Y(0)); x.lineTo(W - pad, Y(0)); x.stroke();
x.strokeStyle = '#1a1a1a'; x.lineWidth = 1.5; x.beginPath();
D.values.forEach((v, i) => {{ if (i === 0) x.moveTo(X(i), Y(v)); else x.lineTo(X(i), Y(v)); }});
x.stroke();
x.fillStyle = '#c89300';
D.values.forEach((v, i) => {{ if (D.flags[i]) {{ x.beginPath(); x.arc(X(i), Y(v), 3.5, 0, 7); x.fill(); }} }});
x.fillStyle = '#555'; x.font = '12px sans-serif';
x.fillText('1999', pad, H - 8); x.fillText('2026', W - 42, H - 8);
x.fillText(max.toFixed(2) + ' °C', 4, pad); x.fillText(min.toFixed(2) + ' °C', 4, H - pad + 4);
</script>
</body>
</html>
"""
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(html)
    print(f"index.html written: {len(months)} months, {len(surprise)} surprise moments")


if __name__ == "__main__":
    main()
