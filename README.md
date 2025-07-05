# AI Hallucination Audit: Citation Mismatches in HIV Prevention Research

[![Paper](https://img.shields.io/badge/Lancet%20Comment-View%20Paper-blue)](https://www.thelancet.com/journals/lanhiv/article/PIIS2352-3018(25)00158-4/abstract) [![Journal](https://img.shields.io/badge/The%20Lancet%20HIV-Journal-red)](https://www.thelancet.com/journals/lanhiv/home)

This repository contains reproducible experiments demonstrating AI hallucination patterns that explain citation mismatches in a published HIV prevention research Comment. We test two disputed claims that appear to originate from the Audere sponsor white paper but are instead attributed to other academic sources.

> **Terminology Note**: Throughout this repository we use "AI hallucination" as a shorthand, even though the behavior we investigate is more nuanced than inventing facts out of thin air. In this case the models conflate two genuine statements of the Audere white paper— for example, AI in Kenya and tele-PrEP in Nigeria—and merge them into a single, misleading claim. The output is therefore better described as *source-blend hallucination* or *AI conflation*, but we keep the familiar term for searchability and to align with the broader literature on LLM errors.

> **Transparency Note**: This investigation follows an open, evidence-based approach. Our [investigation log](docs/investigation_log.md) documents our evolving understanding, uncertainties, and commitment to following evidence wherever it leads.

## Background

We identified apparent citation mismatches in a published Lancet HIV Comment where key sentences do not match their cited sources. Two claims stood out:

1. **Kenya + Nigeria tele-PrEP claim**: *"In Kenya and Nigeria, AI powers telemedicine-based PrEP services that eliminate the need for frequent clinic visits."*
2. **Supply forecasting claim**: *"Predictive models could further enhance these programmes by helping providers identify individuals at greatest risk of HIV acquisition, forecast supply needs, and target outreach efforts more effectively."*

Both sentences cite peer-reviewed academic papers that do not contain these claims. However, the Audere sponsor white paper (which is cited elsewhere in the Comment) contains both phrases. Our experiments test whether AI summarization of this white paper reproduces the disputed sentences when they are incorrectly attributed to other sources.

### Why this matters

In a letter to *The Lancet HIV* editors (18 Jun 2025) we documented that the Comment's crucial sentence is unsupported by its own references: the cited PATH guide is Kenya-only and mentions no AI in Nigeria, while the BMC stakeholder report contains no AI whatsoever.  Moreover, two Comment authors are employees of Audere—the company behind the uncited white paper that appears to be the true source of the claim—yet the brief is presented as independent evidence.  We worry that overstating the real-world maturity of AI-enabled PrEP delivery could mislead policy-makers and funders.  This repository therefore aims to make the provenance of that sentence transparent and testable.

## Experiment 1: Kenya + Nigeria Tele-PrEP Claim

### Hypothesis
The sentence citing the PATH ePrEP guide actually originates from AI summarization of the Audere white paper, which mentions AI in Kenya and tele-PrEP in Nigeria separately.

### Key Findings

1. **Systematic conflation of Kenya & Nigeria.**  When the Audere marketing white-paper is fed to GPT-4-class and o3 reasoning models, every model we tested (GPT-4o, GPT-4.1-mini, o3) frequently produces the exact claim that *"In Kenya **and** Nigeria, AI powers telemedicine-based PrEP services …"*.  
2. **No hallucination from the cited source.**  Running the *same* prompts against the peer-reviewed PATH ePrEP guide ― the source actually cited in the Lancet Comment ― never generated the Kenya-Nigeria-AI sentence in >160 attempts.  
3. **Evidence of source mis-attribution.**  The patterns we observed suggest the sentence in the Lancet paper may have originated from an AI summary of the *Audere* white paper rather than from the scholarly sources it cites.  This analysis provides evidence consistent with "citation laundering".
4. **Ambiguity drives hallucination.**  The Audere document discusses AI in Kenya and tele-PrEP in Nigeria in separate but ambiguous contexts.  LLMs routinely fuse those ideas into a single, more concise claim.

## Experiment 2: Supply Forecasting Claim

### Hypothesis  
The sentence about predictive models to "forecast supply needs" cites Balzer et al. (CID 2020) but actually originates from the Audere white paper, which contains this phrase.

### Key Findings

When asked to generate text about predictive models in HIV prevention, LLMs showed dramatically different patterns depending on their source material. The Balzer et al. paper cited in the Comment never triggered any mentions of supply forecasting across 70 test generations, while the Audere white paper consistently produced this exact phrase. Most revealing was our discovery that Audere itself misinterprets its own McKinsey citation: the referenced McKinsey data actually shows supply-chain management is among the least effective AI applications, undermining rather than supporting the supply forecasting claim.

## Quick Start

### Setup (One-Time)

```bash
# 1. Clone and enter the repository
git clone <repository-url>
cd kenya-nigeria-prep-hallucination-audit

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Add your OpenAI API key
export OPENAI_API_KEY="sk-your-actual-key-here"
# Or create a .env file: echo "OPENAI_API_KEY=sk-your-key" > .env
```

### View Existing Results (No API Key Needed)

```bash
# See summary stats for Kenya+Nigeria experiment
python scripts/analyze_results.py results/final

# See summary stats for Supply Forecasting experiment  
python scripts/predictive_models/analyze_predictive_results.py
```

## 📋 Full Reproduction Workflow

Follow these steps **exactly** to rebuild every figure and CSV in the `docs/` write-ups.  (💡 Replace `<SEEDS>` with your preferred run size – 10 for a quick check, 100–1000 for the numbers reported in the paper.)

### 0. Environment (only once)
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt          # installs openai, tqdm, pdfminer.six, etc.
export OPENAI_API_KEY="sk-…"             # or put into .env
```

### 1. Kenya + Nigeria Tele-PrEP Experiment
Run **both** source texts so we can contrast the hallucination rate.

```bash
# 1-A  Audere white-paper (suspected source)
python scripts/summarize_test.py \
       --src source_materials/audere-whitepaper.md \
       --model gpt-4o-2024-11-20 \
       --seeds <SEEDS>

# 1-B  PATH ePrEP guide (the paper actually cites this)
python scripts/summarize_test.py \
       --src source_materials/eprep-source.md \
       --model gpt-4o-2024-11-20 \
       --seeds <SEEDS>

# Replicate with other models
for M in gpt-4.1-mini-2025-04-14 o3-2025-04-16; do
    python scripts/summarize_test.py --src source_materials/audere-whitepaper.md --model $M --seeds <SEEDS>
    python scripts/summarize_test.py --src source_materials/eprep-source.md      --model $M --seeds <SEEDS>
done
```

Aggregate stats (combines every `results_*.csv` in the current dir):
```bash
python scripts/analyze_results.py
```
This writes `hallucination_stats_<timestamp>.csv`.

To see the delta between Audere vs PATH runs:
```bash
python scripts/diff_stats.py <AUDERE_STATS.csv> <PATH_STATS.csv>
```
Both files are in the directory created above; pick the two matching timestamps.

### 2. Supply-Forecasting Experiment
We run **three experimental conditions—cited paper (Balzer), sponsor paper (Audere), and a no-source control**—and test each with two prompt variants (`short`, `bullets`).

```bash
# 2-A  Cited paper (Balzer et al.)
python scripts/predictive_models/run_predictive_test.py \
       --model gpt-4o-2024-11-20 \
       --prompt-type short \
       --seeds <SEEDS>
python scripts/predictive_models/run_predictive_test.py \
       --model gpt-4o-2024-11-20 \
       --prompt-type bullets \
       --seeds <SEEDS>

# 2-B  Sponsor white-paper (Audere)
python scripts/predictive_models/run_predictive_test.py \
       --model gpt-4o-2024-11-20 \
       --prompt-type short \
       --src-file source_materials/audere-whitepaper.md \
       --seeds <SEEDS>
python scripts/predictive_models/run_predictive_test.py \
       --model gpt-4o-2024-11-20 \
       --prompt-type bullets \
       --src-file source_materials/audere-whitepaper.md \
       --seeds <SEEDS>

# 2-C  No source (control)
python scripts/predictive_models/run_predictive_test.py \
       --model gpt-4o-2024-11-20 \
       --prompt-type short \
       --no-source \
       --seeds <SEEDS>
python scripts/predictive_models/run_predictive_test.py \
       --model gpt-4o-2024-11-20 \
       --prompt-type bullets \
       --no-source \
       --seeds <SEEDS>
```

Aggregate:
```bash
python scripts/predictive_models/analyze_predictive_results.py
```
Outputs `predictive_results/predictive_stats_<timestamp>.csv` with hit rates for each run.

### 3. Inspect The Outputs

| What | Where | Notes |
|------|-------|-------|
| Raw Kenya+Nigeria generations | `results_*.csv` | One CSV per model × prompt × source |
| Kenya+Nigeria summary stats | `hallucination_stats_*.csv` | Created by `analyze_results.py` |
| Supply-forecast raw generations | `predictive_results/predictive_*.csv` | One CSV per model × prompt × condition |
| Supply-forecast stats | `predictive_results/predictive_stats_*.csv` | Created by `analyze_predictive_results.py` |

All numbers shown in `docs/hallucination_report.md` and `docs/hallucination_supply_forecast.md` were produced exactly this way with:
```
# Kenya+Nigeria  : <SEEDS>=1000 (GPT-4o) 20/20 (4-mini) 5/5 (o3)
# Supply-forecast: <SEEDS>=100  (GPT-4o) 100/100 (4-mini) 25/25 (o3)
```

**Tip**: OpenAI now grants 1 M–10 M free tokens if you opt into their optional "share data for research" program, letting you run every experiment in this repo for free with all compatible models (<https://help.openai.com/en/articles/10306912-sharing-feedback-evaluation-and-fine-tuning-data-and-api-inputs-and-outputs-with-openai>).

### What the Experiments Do

1. **Kenya+Nigeria Experiment**: Tests if LLMs generate the disputed claim *"In Kenya and Nigeria, AI powers telemedicine..."* when given the Audere sponsor document vs. the cited academic sources.

2. **Supply Forecasting Experiment**: Tests if LLMs generate *"forecast supply needs"* language when given different source materials.

Both experiments output CSV files with the generated text and statistical summaries showing hallucination rates.

## Documentation

- **[Kenya+Nigeria Analysis](docs/hallucination_report.md)** - Original experiment findings
- **[Supply Forecasting Analysis](docs/hallucination_supply_forecast.md)** - Second experiment findings  
- **[Conflict-of-Interest Analysis](docs/undisclosed_audere_coi.md)** - Detailed audit of undisclosed author ties and COI disclosure requirements  
- **[Investigation Log](docs/investigation_log.md)** - Transparent timeline of investigation
- **[Source Materials](source_materials/)** - All original documents

Both experiments provide empirical evidence suggesting that the disputed sentences in the published Comment may have originated from the Audere sponsor document rather than from the cited academic sources.

## Limitations and Request for Replication

These results are **not definitive**. We welcome replication attempts and especially
encourage sharing of **negative or contradictory findings**. If you spot an
error or have evidence that challenges our assumptions, please open an issue or
pull request so the community can review it.

## Legal and Conduct Disclaimer

This repository presents our best understanding of publicly available
information. The analysis and interpretations herein are offered in good faith
for scholarly discussion. We do not claim to provide legal advice, and no part
of this project should be read as a personal attack on any individual. If you
identify errors or believe statements are inaccurate, please let us know so we
can correct the record.

