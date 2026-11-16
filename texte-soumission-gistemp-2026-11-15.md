# NASA Space Apps 2026 — Texte de soumission (Jukebox + GISTEMP)
Prêt à coller dans l'onglet Project de l'équipe. Défi : **The Earth Information Jukebox**.
Équipe solo (volgat), événement local Windsor. Soumission due dim. 15 nov. 23h59 HE.
Version réécrite le 15 nov. 19h40 pour le champ Project Details (répond aux
questions du formulaire : quoi, comment, bénéfices, impact, outils, créativité).
Aucune mention d'assistant IA dans le texte de soumission (décision de Mike).

---

## Summary (champ Summary, 175 mots, 979 caractères)

Hear the Warming turns 27 years of NASA global temperature data into 60 seconds of sound. Each month from January 1999 to October 2026 is one note: a higher temperature anomaly plays a higher pitch, and months that stand out from their 25-month neighbourhood play louder, with a brighter note. In one minute you hear the long rise, the El Niño spike of 2015–16, the record heat of 2023, and October 2026 — the hottest month in the whole record at +1.55 °C. The page also shows the curve and the list of flagged months, so you can see what you just heard.

The challenge asks for sound instead of sight, so the project makes Earth science accessible to people who cannot read a chart — and immediate for everyone else. The data is NASA GISTEMP v4 (334 monthly values). The method is plain Python, standard library only: a rolling z-score (25-month window, threshold z ≥ 2.0) flags 33 surprise months. All code, data and audio are open source (Apache 2.0) in the linked repository.

---

## Project Details (champ Project Details)

**What it does and how it works:**
Hear the Warming is a web page that plays 27 years of NASA global temperature data as sound. Each month from January 1999 to October 2026 is one note: a higher temperature anomaly plays a higher pitch. Months that stand out from their 25-month neighbourhood play louder, with a brighter note. In 60 seconds you hear the long rise, the El Niño spike of 2015–16, the record heat of 2023, and October 2026 — the hottest month in the whole record at +1.55 °C. The page also shows the curve with gold dots on the flagged months and the list of moments, so you can see what you just heard.

**Data:**
NASA GISTEMP v4 (GISS Surface Temperature Analysis), global land-ocean temperature index, monthly anomaly vs the 1951–1980 baseline, in °C. Source file GLB.Ts+dSST.csv. 334 monthly values, January 1999 – October 2026. No other dataset.

**Method and tools:**
Plain Python, standard library only. A rolling z-score (25-month window, threshold z ≥ 2.0) flags 33 "surprise" months out of 334. The mapping from anomaly to pitch is linear and chosen for listening. No proprietary code, no third-party model, no closed-source component. All code, data and audio are in the linked repository (open source, Apache 2.0).

**Validation — what we heard:**
The flagged months cluster on known real events, not on noise:
- El Niño 2015–16: October 2015 – March 2016, up to +1.36 °C (Feb 2016).
- Record heat 2023: March and July–November 2023, including +1.48 °C (Sep 2023).
- 2026: August +1.42 °C and October +1.55 °C — October 2026 is the highest value in the entire series.
- Earlier warm clusters: late 2001 – early 2002, January 2007, March 2010, and 2019 – early 2020.

**Creativity:**
The challenge asks to translate sight into sound. Here the data itself becomes the sound — no melody composed, no music added. The listener hears the trend and the outliers directly, in one minute. Sound reaches people a chart cannot reach.

**Intended impact:**
27 years of warming is a slow curve that eyes glaze over. Hearing it — the baseline rising month after month, the spikes standing out — makes the change immediate. It works for people who cannot read a chart, for classrooms, and for anyone who understands better by listening than by looking.

**Limitations (stated honestly):**
The detector flags deviations in either direction, so it also catches cold dips (January 2008, December 2010, February 2021) — a "surprise" is not heat alone. Because the series trends upward, a rolling z-score flags many recent points; 33 moments is too many to narrate one by one, so the submission names the clusters instead. The pitch scale is a listening choice, not a physical scale.

**Links:**
- Demo (audio + curve + moments): https://volgat.github.io/nasa-jukebox-2026/
- Code, data and audio (open source): https://github.com/Volgat/nasa-jukebox-2026
