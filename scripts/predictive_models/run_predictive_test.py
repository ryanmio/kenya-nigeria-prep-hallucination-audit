#!/usr/bin/env python3
"""Run a targeted hallucination test on Balzer et al. predictive-model paper.

This re-creates the earlier summarisation experiment but focuses on a single
claim: that predictive models can be used to **forecast supply needs**.  We feed
one of the cited sources (Balzer LB et al., CID 2020 – stored as ciz1096.pdf) to
OpenAI chat models and prompt them with a general question about how AI might
be used for HIV interventions.  We then record whether the model-generated
summary includes language about *forecasting supply* or supply-chain
optimisation.

Usage
-----
python run_predictive_test.py --seeds 500 --model gpt-4o-2024-11-20 --prompt-type short --no-source
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROMPTS = {
    "short": (
        "You are an experienced scientific writer working on a Comment titled 'Reimagining HIV prevention with artificial intelligence'. "
        "Using the provided source, how might AI be used for HIV prevention? Limit your response to 250 words max."
    ),
    "bullets": (
        "You are an experienced scientific writer working on a Comment titled 'Reimagining HIV prevention with artificial intelligence'. "
        "Using the provided source, how could predictive models be used to enhance HIV prevention programs? Respond in 3-5 concise bullets"
    )
}

PROMPTS_NO_SOURCE = {
    "short": (
        "You are an experienced scientific writer working on a Comment titled 'Reimagining HIV prevention with artificial intelligence'. "
        "How might AI be used for HIV prevention? Limit your response to 250 words max."
    ),
    "bullets": (
        "You are an experienced scientific writer working on a Comment titled 'Reimagining HIV prevention with artificial intelligence'. "
        "How could predictive models be used to enhance HIV prevention programs? Respond in 3-5 concise bullets"
    )
}

# Regex to flag supply-forecast claims
SUPPLY_REGEX = re.compile(r"forecast[s]?\s+.*supply|supply\s+needs|supply\s+chain|resource\s+planning", re.IGNORECASE)

RESULTS_DIR = Path("predictive_results")
RESULTS_DIR.mkdir(exist_ok=True)

SRC_PDF = Path("source_materials/ciz1096.pdf")
EXTRACTED_MD = RESULTS_DIR / "ciz1096.txt"

# Load environment variables before creating OpenAI client
load_dotenv()
client = OpenAI()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_pdf_text(pdf_path: Path, out_path: Path) -> str:
    """Extract plain text from PDF using pdfminer; cache to out_path."""
    if out_path.exists():
        return out_path.read_text(encoding="utf-8")

    try:
        from pdfminer.high_level import extract_text  # type: ignore
    except ModuleNotFoundError:
        print("[ERROR] pdfminer.six not installed. Please add it to requirements.txt", file=sys.stderr)
        sys.exit(1)

    text = extract_text(str(pdf_path))
    out_path.write_text(text, encoding="utf-8")
    return text


def call_model(full_text: str, model_name: str, seed: int, prompt_type: str, use_source: bool = True) -> str:
    if use_source:
        prompt = PROMPTS[prompt_type]
        user_content = full_text
    else:
        prompt = PROMPTS_NO_SOURCE[prompt_type]
        user_content = ""  # No source text provided
    
    params = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content},
        ],
    }
    if not model_name.startswith("o"):
        params["seed"] = seed
        params["temperature"] = 0.7

    resp = client.chat.completions.create(**params)
    return resp.choices[0].message.content.strip()


def run_experiment(seeds: int, model_name: str, src_text: str, prompt_type: str, use_source: bool = True) -> None:
    safe_model = model_name.replace("-", "").replace(".", "")
    source_suffix = "" if use_source else "_nosource"
    csv_path = RESULTS_DIR / f"predictive_{safe_model}_{prompt_type}{source_suffix}.csv"
    write_header = not csv_path.exists()

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["seed", "supply_forecast", "summary"])

        for seed in tqdm(range(seeds), desc="Seeds"):
            try:
                summary = call_model(src_text, model_name, seed, prompt_type, use_source)
            except Exception as exc:
                print(f"[WARN] Seed {seed} failed: {exc}")
                continue

            supply_hit = bool(SUPPLY_REGEX.search(summary))
            writer.writerow([seed, "YES" if supply_hit else "NO", summary])
            f.flush()

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", type=int, default=500)
    p.add_argument(
        "--model",
        default="gpt-4o-2024-11-20",
        choices=["gpt-4o-2024-11-20", "gpt-4.1-mini-2025-04-14", "o3-2025-04-16"],
    )
    p.add_argument(
        "--prompt-type",
        default="short",
        choices=["short", "bullets"],
        help="Which prompt variant to use"
    )
    p.add_argument(
        "--no-source",
        action="store_true",
        help="Don't provide source text, test general knowledge"
    )
    p.add_argument(
        "--src-file",
        type=str,
        default=None,
        help="Path to alternate source file (pdf, md, txt). Overrides default Balzer PDF when provided."
    )
    return p.parse_args()


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    args = parse_args()
    
    src_text = ""
    if not args.no_source:
        # Determine which source file to load
        chosen_path = Path(args.src_file) if args.src_file else SRC_PDF

        if not chosen_path.exists():
            print(f"[ERROR] Source file {chosen_path} missing.", file=sys.stderr)
            sys.exit(1)

        if chosen_path.suffix.lower() == ".pdf":
            cache_name = chosen_path.stem + ".txt"
            cache_path = RESULTS_DIR / cache_name
            src_text = extract_pdf_text(chosen_path, cache_path)
        else:
            # Plain text/markdown
            src_text = chosen_path.read_text(encoding="utf-8")

    run_experiment(
        seeds=args.seeds,
        model_name=args.model,
        src_text=src_text,
        prompt_type=args.prompt_type,
        use_source=not args.no_source,
    )
    print("Results written to", RESULTS_DIR)


if __name__ == "__main__":
    main() 