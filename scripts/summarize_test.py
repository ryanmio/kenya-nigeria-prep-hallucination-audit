#!/usr/bin/env python3
"""Summarise the Audere white-paper multiple times and detect hallucinations.

Usage
-----
python summarize_test.py --seeds 1000 --model gpt-4o-2024-11-20
python summarize_test.py --seeds 1000 --model o3-2025-04-16
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Try to use RapidFuzz for speed; fall back to difflib if unavailable
try:
    from rapidfuzz.fuzz import ratio as fuzz_ratio  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    import difflib

    def fuzz_ratio(a: str, b: str) -> int:  # type: ignore
        """Basic Levenshtein ratio fallback using difflib."""
        return int(difflib.SequenceMatcher(None, a, b).ratio() * 100)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CANONICAL_SENTENCE = (
    "In Kenya and Nigeria, AI powers telemedicine-based PrEP services that "
    "eliminate the need for frequent clinic visits"
)

# Prompt variants to stress-test hallucination behaviour.
GROUNDING_PREFIX = (
    "You are an experienced scientific writer. Base your answer ONLY on the user-supplied text.\n\n"
)

PROMPT_VARIANTS = [
    ("africa", GROUNDING_PREFIX + "Provide 2-3 examples of innovative AI approaches underway in Africa."),
    ("global", GROUNDING_PREFIX + "Provide 2-3 examples of innovative AI approaches related to telemedicine and where they are being used."),
    ("tele_one", GROUNDING_PREFIX + "Provide 1 specific example of an innovative AI approach underway in Africa relating to PrEP and/or Telemedicine."),
    ("tele_multi", GROUNDING_PREFIX + "How and where is AI being used to improve telemedicine? Respond in 1-3 sentences."),
]

# Positive look-ahead regex that ensures all four keywords appear **in order**
STRICT_REGEX = re.compile(
    r"(?i)Kenya[^.]*Nigeria[^.]*AI[^.]*telemedicine", re.IGNORECASE
)
# For loose tier: all four keywords anywhere (order-agnostic)
LOOSE_REGEX = re.compile(
    r"(?is)(?=.*Kenya)(?=.*Nigeria)(?=.*AI)(?=.*telemedicine)", re.IGNORECASE
)

SRC_MD_PATH = Path("source_materials/audere-whitepaper.md")
RESULTS_CSV = Path("results.csv")

# ---------------------------------------------------------------------------
# Helper dataclass
# ---------------------------------------------------------------------------
@dataclass
class EvalOutcome:
    tier: str  # STRICT / LOOSE / EMBED / -
    fuzz: int  # 0-100

# ---------------------------------------------------------------------------
# Model call
# ---------------------------------------------------------------------------

# Initialize OpenAI client
client = OpenAI()

def call_model(full_text: str, model_name: str, seed: int, system_prompt: str) -> str:
    """Send text to the model and return the one-sentence summary."""
    params = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_text},
        ],
    }

    # Only GPT-4 family supports seed / temperature currently
    if not model_name.startswith("o"):
        params["seed"] = seed
        params["temperature"] = 0.7

    response = client.chat.completions.create(**params)
    return response.choices[0].message.content.strip()

# ---------------------------------------------------------------------------
# Evaluation (simple regex-based)
# ---------------------------------------------------------------------------

def evaluate_summary(summary: str) -> EvalOutcome:
    """Classify summary based on Kenya+Nigeria+AI+telemedicine presence for STRICT/LOOSE."""
    text = summary.strip()

    if STRICT_REGEX.search(text):
        tier = "STRICT"
    elif LOOSE_REGEX.search(text):
        tier = "LOOSE"
    else:
        tier = "-"

    return EvalOutcome(tier=tier, fuzz=fuzz_ratio(text, CANONICAL_SENTENCE))

# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run_experiment(seeds: int, model_name: str, prompt_label: str, system_prompt: str, src_path: Path) -> None:
    if not src_path.exists():
        print(f"[ERROR] Required source file '{src_path}' not found.", file=sys.stderr)
        sys.exit(1)

    full_text = src_path.read_text(encoding="utf-8")

    # CSV name per prompt variant
    safe_model = model_name.replace("-", "").replace(".", "")
    csv_path = Path(f"results_{safe_model}_{prompt_label}.csv")
    write_header = not csv_path.exists()
    csv_file = csv_path.open("a", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)

    if write_header:
        csv_writer.writerow(["seed", "tier", "fuzz_ratio", "summary"])

    # Track first hits
    first_hit: Dict[str, str] = {}

    for seed in tqdm(range(seeds), desc="Seeds"):
        try:
            summary = call_model(full_text, model_name, seed, system_prompt)
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] Seed {seed} failed: {exc}")
            continue

        outcome = evaluate_summary(summary)
        csv_writer.writerow([seed, outcome.tier, outcome.fuzz, summary])
        csv_file.flush()

        # Print first hit per tier
        if outcome.tier not in first_hit and outcome.tier in {"STRICT", "LOOSE", "EMBED"}:
            first_hit[outcome.tier] = summary
            print("\n" + "=" * 60)
            print(f"FIRST {outcome.tier} HIT @ seed {seed}\n{summary}\n")
            print("=" * 60)

    csv_file.close()
    print("Experiment complete. Results saved to", csv_path)


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect hallucination in model summaries.")
    parser.add_argument(
        "--seeds",
        type=int,
        default=1000,
        help="Number of seeds / generations to test (default: 1000)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-2024-11-20",
        choices=["gpt-4o-2024-11-20", "gpt-4.1-mini-2025-04-14", "o3-2025-04-16"],
        help="Model to query (default: gpt-4o-2024-11-20)",
    )
    parser.add_argument(
        "--src",
        type=str,
        default="source_materials/audere-whitepaper.md",
        help="Path to markdown file containing source text (default: source_materials/audere-whitepaper.md)",
    )
    return parser.parse_args()


def main() -> None:
    # Load .env file if present
    load_dotenv()

    # Verify OPENAI_API_KEY is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY is not set. Please check your .env file.", file=sys.stderr)
        sys.exit(1)

    args = parse_args()
    src_path = Path(args.src)
    for prompt_label, system_prompt in PROMPT_VARIANTS:
        run_experiment(seeds=args.seeds, model_name=args.model, prompt_label=prompt_label, system_prompt=system_prompt, src_path=src_path)


if __name__ == "__main__":
    main() 