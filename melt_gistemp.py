#!/usr/bin/env python3
"""
Melt NASA GISTEMP v4 wide table (one row per year, Jan..Dec columns) into a
long date,value series that sonify_mopitt.py can read.

Source (verified live 2026-11-15 ~11h21 Toronto):
  https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv
  Land-Ocean global means, monthly temperature anomaly vs 1951-1980, °C.
  Values are anomalies (e.g. .48 = +0.48 °C). "***" = missing month.
  Coverage in the file used here: Jan 1999 - Oct 2026 (Nov-Dec 2026 missing).

Usage:
  python3 melt_gistemp.py gistemp_1999_2026_wide.csv --out gistemp_monthly.csv
  python3 sonify_mopitt.py gistemp_monthly.csv --out gistemp_jukebox.wav --seconds 60
"""
import argparse
import csv

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def main():
    p = argparse.ArgumentParser(description="Melt GISTEMP wide table to long series.")
    p.add_argument("wide_csv")
    p.add_argument("--out", default="gistemp_monthly.csv")
    args = p.parse_args()

    rows = []
    with open(args.wide_csv, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            year = int(r["Year"])
            for i, m in enumerate(MONTHS, start=1):
                v = (r[m] or "").strip()
                if v in ("", "***"):
                    continue
                rows.append((f"{year}-{i:02d}-01", float(v)))
    rows.sort()
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "value"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} monthly values to {args.out} "
          f"({rows[0][0]} to {rows[-1][0]}).")


if __name__ == "__main__":
    main()
