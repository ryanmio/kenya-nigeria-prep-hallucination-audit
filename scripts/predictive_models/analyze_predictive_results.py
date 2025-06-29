#!/usr/bin/env python3
"""Aggregate supply-forecast hallucination stats from predictive_results CSVs.

Usage:
    python analyze_predictive_results.py
Produces a CSV in predictive_results/ with hit counts and percentage for each model.
"""
from pathlib import Path
import csv
from datetime import datetime

RESULTS_DIR = Path("predictive_results")


def analyse(csv_path: Path):
    total = 0
    supply_hits = 0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip rows that don't have the supply_forecast column (like stats files)
            if "supply_forecast" not in row:
                continue
            total += 1
            if row["supply_forecast"] == "YES":
                supply_hits += 1
    rate = (supply_hits / total * 100) if total else 0.0
    return total, supply_hits, rate


def main() -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = RESULTS_DIR / f"predictive_stats_{ts}.csv"

    with out_path.open("w", newline="", encoding="utf-8") as outf:
        writer = csv.writer(outf)
        writer.writerow(["model", "total", "supply_hits", "percent"])

        for csv_path in RESULTS_DIR.glob("predictive_*.csv"):
            # Skip files that are already stats files
            if "stats" in csv_path.name:
                continue
            total, hits, pct = analyse(csv_path)
            model = csv_path.stem.replace("predictive_", "")
            writer.writerow([model, total, hits, f"{pct:.1f}"])

    print("Stats written to", out_path)


if __name__ == "__main__":
    main() 