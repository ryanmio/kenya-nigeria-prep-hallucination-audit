#!/usr/bin/env python3
"""Aggregate hallucination counts across result CSVs.

Usage:
    python analyze_results.py [directory]

If no directory is specified, searches current directory for results_*.csv files.
Outputs a small table to console: prompt label, total summaries, hallucination hits, %.
"""
from pathlib import Path
import csv
import sys
from datetime import datetime

PROMPT_MAP = {
    "africa": "Provide 3-5 examples of innovative AI approaches underway in Africa.",
    "global": "Provide 3-5 examples of innovative AI approaches underway.",
    "one_sentence": "In ONE sentence, summarise innovative AI approaches from the text.",
    "tele_one": "In ONE sentence, summarise innovative AI-powered telemedicine approaches from the text.",
    "tele_multi": "How and where is AI being used to improve telemedicine? Respond in 1-3 sentences.",
}

def analyze(csv_path: Path):
    total = 0
    hits = 0
    seed_values = []
    with csv_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            seed_values.append(int(row['seed']))
            summ = row['summary'].lower()
            if ('nigeria' in summ) and ('kenya' in summ) and ('ai' in summ):
                hits += 1
    rate = hits / total * 100 if total else 0
    return total, hits, rate, seed_values


def main():
    # Check if directory argument provided
    search_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    
    if not search_dir.exists():
        print(f"[ERROR] Directory '{search_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(f"hallucination_stats_{ts}.csv")

    with out_path.open("w", newline="", encoding="utf-8") as outf:
        writer = csv.writer(outf)
        writer.writerow([
            "model",
            "prompt_label",
            "prompt_text",
            "total",
            "hallucinations",
            "percent",
            "seed_count",
        ])

        csv_files = list(search_dir.glob("results_*.csv"))
        if not csv_files:
            print(f"[WARN] No results_*.csv files found in '{search_dir}'", file=sys.stderr)
            
        for csv_path in csv_files:
            total, hits, rate, seed_values = analyze(csv_path)

            # filename pattern: results_<model>_<prompt>.csv
            parts = csv_path.stem.split("_", 2)
            if len(parts) >= 3:
                _prefix, model_label, prompt_label = parts[0], parts[1], parts[2]
            else:
                model_label = "unknown"
                prompt_label = csv_path.stem.replace("results_", "")

            writer.writerow([
                model_label,
                prompt_label,
                PROMPT_MAP.get(prompt_label, prompt_label),
                total,
                hits,
                f"{rate:.1f}",
                len(seed_values),
            ])

    print("Stats written to", out_path)

if __name__ == '__main__':
    main() 