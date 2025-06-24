#!/usr/bin/env python3
"""Create delta stats between two hallucination stats CSV files.

Usage:
    python diff_stats.py old.csv new.csv
Outputs a CSV diff_<timestamp>.csv with same columns but delta (new-old) for total, hallucinations, seed_count; percent recalculated.
"""
import csv
import sys
from pathlib import Path
from datetime import datetime

if len(sys.argv) != 3:
    print("Usage: python diff_stats.py old.csv new.csv")
    sys.exit(1)

old_path = Path(sys.argv[1])
new_path = Path(sys.argv[2])

if not old_path.exists() or not new_path.exists():
    print("One of the input files does not exist.")
    sys.exit(1)

# index by (model, prompt_label)
old_stats = {}
with old_path.open() as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["model"], row["prompt_label"])
        old_stats[key] = row

rows = []
with new_path.open() as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["model"], row["prompt_label"])
        o = old_stats.get(key)
        total = int(row["total"]) - (int(o["total"]) if o else 0)
        hits = int(row["hallucinations"]) - (int(o["hallucinations"]) if o else 0)
        seeds = int(row["seed_count"]) - (int(o["seed_count"]) if o else 0)
        percent = round(hits / total * 100, 1) if total else 0.0
        rows.append({
            "model": row["model"],
            "prompt_label": row["prompt_label"],
            "prompt_text": row["prompt_text"],
            "total": total,
            "hallucinations": hits,
            "percent": percent,
            "seed_count": seeds,
        })

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = Path(f"hallucination_delta_{ts}.csv")
with out_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["model", "prompt_label", "prompt_text", "total", "hallucinations", "percent", "seed_count"])
    writer.writeheader()
    writer.writerows(rows)
print("Delta stats written to", out_path) 