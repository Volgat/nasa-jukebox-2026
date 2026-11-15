# Hear the Warming — 27 Years of Global Temperature in 60 Seconds

NASA Space Apps Challenge 2026 — **The Earth Information Jukebox** — solo project by
volgat (Windsor local event).

**Listen:** https://volgat.github.io/nasa-jukebox-2026/

## What it is

A web page that plays 27 years of NASA global temperature data as sound.
Each month from January 1999 to October 2026 is one note: a higher temperature
anomaly plays a higher pitch, and months that stand out from their 25-month
neighbourhood play louder, with a brighter note. In 60 seconds you hear the
long rise, the El Niño spike of 2015–16, the record heat of 2023, and October
2026 — the hottest month in the record at +1.55 °C.

## Data

NASA GISTEMP v4 (GISS Surface Temperature Analysis), global land-ocean
temperature index, monthly anomaly vs the 1951–1980 baseline, in °C.
Source file: `GLB.Ts+dSST.csv`,
https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv
334 monthly values, January 1999 – October 2026. No other dataset.

## Method

Plain Python, standard library only. A rolling z-score (25-month window,
threshold z ≥ 2.0) flags 33 "surprise" months out of 334. No proprietary code,
no third-party model.

## Files

- `index.html` — the demo page (audio player + curve + flagged months)
- `gistemp_jukebox.wav` — the 60-second sonification (334 notes)
- `gistemp_monthly.csv` — 334 monthly values, Jan 1999 – Oct 2026
- `gistemp_events.csv` — the 33 flagged "surprise" months
- `gistemp_1999_2026_wide.csv` — the GISTEMP table as downloaded
- `melt_gistemp.py` — wide table → long monthly series
- `sonify_mopitt.py` — the sonification script (standard library only)
- `build_page.py` — regenerates `index.html` from the CSVs
- `slides.html` — the 6-slide demo deck (chart + audio player)
- `build_slides.py` — regenerates `slides.html` from the CSVs
- `texte-soumission-gistemp-2026-11-15.md` — the submission text (in French notes + English text)

## AI assistance (Super Intelligence disclosure)

The code and the submission text were written with the assistance of an AI
coding assistant (Muse). The audio and the chart are computed
deterministically from the NASA data, not AI-generated. No AI-generated
images, video or music are used.

## Honest limits

The detector flags deviations in either direction, so it also catches cold dips
(Jan 2008, Dec 2010, Feb 2021). Because the series trends upward, a rolling
z-score flags many recent points; 33 moments is too many to narrate one by one,
so the submission names the clusters instead. The pitch scale is a listening
choice, not a physical scale.

## License

Apache 2.0.
