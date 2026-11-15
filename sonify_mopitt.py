#!/usr/bin/env python3
"""
NASA Space Apps 2026 (Windsor) — The Earth Information Jukebox, starter kit.
Sonifies a long MOPITT carbon-monoxide time series (1999-2026, CSV from the
Canadian Space Agency open-data portal) into a short WAV "jukebox track".

What it does, honestly:
  - Reads any CSV with a date column and a numeric value column (columns are
    auto-detected; MOPITT's exact header names are NOT assumed, so check the
    printed column mapping before trusting the output).
  - Maps each value to a pitch: low CO = low note, high CO = high note.
  - Marks "surprise" moments with a louder, brighter note: a point whose
    value deviates from its rolling neighbourhood by more than a threshold
    (rolling z-score). This is a simple, deterministic statistic — it is NOT
    the KEEP engine and no KEEP code is used or distributed here. The project
    stands on its own open code.
  - Writes events.csv (date, value, z-score, surprise flag) so the submission
    can name the exact moments it claims (wildfire peaks, COVID dip, ...).

Usage:
  python3 sonify_mopitt.py mopitt.csv --out co_jukebox.wav --seconds 60
  python3 sonify_mopitt.py --demo --out demo.wav        # no CSV needed, test the sound first
  python3 sonify_mopitt.py mopitt.csv --value-column CO --date-column DATE

Only the Python standard library is used. No install needed.
"""

import argparse
import csv
import math
import random
import struct
import sys
import wave
from datetime import date, timedelta

SAMPLE_RATE = 44100


def parse_args():
    p = argparse.ArgumentParser(description="Sonify a CO time series into a WAV file.")
    p.add_argument("csv_path", nargs="?", help="CSV file (date + numeric value columns)")
    p.add_argument("--demo", action="store_true", help="Generate a synthetic demo series instead of reading a CSV")
    p.add_argument("--out", default="co_jukebox.wav", help="Output WAV file (default: co_jukebox.wav)")
    p.add_argument("--events-out", default="events.csv", help="Output events CSV (default: events.csv)")
    p.add_argument("--seconds", type=float, default=60.0, help="Target length in seconds (default: 60)")
    p.add_argument("--date-column", default=None, help="Name of the date column (auto-detected if omitted)")
    p.add_argument("--value-column", default=None, help="Name of the numeric value column (auto-detected if omitted)")
    p.add_argument("--z-threshold", type=float, default=2.0, help="Z-score above which a point is a surprise (default: 2.0)")
    p.add_argument("--window", type=int, default=25, help="Rolling window for the z-score (default: 25 points)")
    return p.parse_args()


def demo_series(n=324):
    """Synthetic monthly series, 1999-2026: slow rise, seasonal wobble,
    a few wildfire spikes and a 2020 dip — only to test the sound."""
    rnd = random.Random(7)
    out = []
    start = date(1999, 1, 1)
    for i in range(n):
        d = date(start.year + (start.month - 1 + i) // 12,
                 (start.month - 1 + i) % 12 + 1, 1)
        v = 100 + 0.15 * i + 8 * math.sin(2 * math.pi * i / 12.0) + rnd.uniform(-3, 3)
        if i in (120, 121, 210, 211):   # wildfire-style spikes
            v += 45
        if 250 <= i <= 258:             # COVID-style dip
            v -= 18
        out.append((d.isoformat(), round(v, 2)))
    return out


def read_series(path, date_col, value_col):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f"No data rows in {path}")
    headers = list(rows[0].keys())

    def pick_date():
        if date_col:
            return date_col
        for h in headers:
            if h.strip().lower() in ("date", "time", "year", "month", "datetime", "timestamp"):
                return h
        return headers[0]

    def pick_value(dcol):
        if value_col:
            return value_col
        for h in headers:
            if h == dcol:
                continue
            try:
                float(str(rows[0][h]).replace(",", "."))
                return h
            except (TypeError, ValueError):
                continue
        raise SystemExit("No numeric value column found. Use --value-column.")

    dcol = pick_date()
    vcol = pick_value(dcol)
    series = []
    for r in rows:
        try:
            v = float(str(r[vcol]).replace(",", "."))
        except (TypeError, ValueError):
            continue
        series.append((str(r[dcol]).strip(), v))
    print(f"Columns used: date={dcol!r} value={vcol!r} — check this mapping matches the file.")
    print(f"Points kept: {len(series)} (from {len(rows)} rows)")
    return series


def surprise_flags(values, window, threshold):
    """Rolling z-score: a point is a surprise if it stands out from its
    neighbourhood. Returns a list of booleans, same length as values."""
    flags = []
    for i, v in enumerate(values):
        if i < window:
            # Not enough neighbourhood yet: never flag the first `window` points.
            flags.append(False)
            continue
        lo = max(0, i - window)
        neigh = values[lo:i] or values[:1]
        mean = sum(neigh) / len(neigh)
        var = sum((x - mean) ** 2 for x in neigh) / len(neigh)
        sd = math.sqrt(var) or 1e-9
        flags.append(abs(v - mean) / sd >= threshold)
    return flags


def midi_to_freq(midi):
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def render(series, flags, seconds):
    """One note per data point, evenly spread over `seconds`.
    Value -> pitch (MIDI 48..84). Surprise -> louder + a fifth above."""
    values = [v for _, v in series]
    vmin, vmax = min(values), max(values)
    span = (vmax - vmin) or 1.0
    n = len(series)
    note_dur = seconds / n
    samples_per_note = max(1, int(SAMPLE_RATE * note_dur))
    frames = bytearray()
    for i, (_, v) in enumerate(series):
        midi = 48 + 36 * (v - vmin) / span
        freq = midi_to_freq(midi)
        amp = 0.45 if flags[i] else 0.28
        freqs = [freq, freq * 1.5] if flags[i] else [freq]
        for s in range(samples_per_note):
            t = s / SAMPLE_RATE
            env = min(1.0, s / (SAMPLE_RATE * 0.01)) * (1.0 - s / samples_per_note)
            sample = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
            frames += struct.pack("<h", int(amp * env * sample * 32767))
    return bytes(frames)


def main():
    args = parse_args()
    if args.demo:
        series = demo_series()
        print("Demo mode: synthetic series, 324 monthly points 1999-2026.")
    else:
        if not args.csv_path:
            sys.exit("Give a CSV file, or use --demo to test the sound first.")
        series = read_series(args.csv_path, args.date_column, args.value_column)
    values = [v for _, v in series]
    flags = surprise_flags(values, args.window, args.z_threshold)

    with open(args.events_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "value", "surprise"])
        for (d, v), flag in zip(series, flags):
            w.writerow([d, v, "YES" if flag else ""])
    n_surprises = sum(flags)
    print(f"Surprise moments: {n_surprises} of {len(series)} points "
          f"(z >= {args.z_threshold}, window {args.window})")
    print(f"Events written to {args.events_out} — name these dates in the submission.")

    audio = render(series, flags, args.seconds)
    with wave.open(args.out, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio)
    print(f"WAV written: {args.out} ({args.seconds:.0f} s, {len(series)} notes, "
          f"one note per data point)")


if __name__ == "__main__":
    main()
