# AI Hallucination Audit: Citation Mismatches in HIV Prevention Research

[![Paper](https://img.shields.io/badge/Lancet%20Comment-View%20Paper-blue)](https://www.thelancet.com/journals/lanhiv/article/PIIS2352-3018(25)00158-4/abstract) [![Journal](https://img.shields.io/badge/The%20Lancet%20HIV-Journal-red)](https://www.thelancet.com/journals/lanhiv/home)

This repository contains reproducible experiments demonstrating AI hallucination patterns that explain citation mismatches in a published HIV prevention research Comment. We test two disputed claims that appear to originate from the Audere sponsor white paper but are instead attributed to other academic sources.

> **🔍 Transparency Note**: This investigation follows an open, evidence-based approach. Our [investigation log](docs/investigation_log.md) documents our evolving understanding, uncertainties, and commitment to following evidence wherever it leads.

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

### Terminology note  
Throughout this repository we use "AI hallucination" as a shorthand, even though the behaviour we investigate is more nuanced than inventing facts out of thin air.  In this case the models **conflate** two genuine statements of the Audere white paper—AI in Kenya and tele-PrEP in Nigeria—and merge them into a single, misleading claim.  The output is therefore better described as *source-blend hallucination* or *AI conflation*, but we keep the familiar term for searchability and to align with the broader literature on LLM errors.

## Experiment 2: Supply Forecasting Claim

### Hypothesis  
The sentence about predictive models to "forecast supply needs" cites Balzer et al. (CID 2020) but actually originates from the Audere white paper, which contains this phrase.

### Key Findings

When asked to generate text about predictive models in HIV prevention, LLMs showed dramatically different patterns depending on their source material. The Balzer et al. paper cited in the Comment never triggered any mentions of supply forecasting across 70 test generations, while the Audere white paper consistently produced this exact phrase. Most revealing was our discovery that Audere itself misinterprets its own McKinsey citation: the referenced McKinsey data actually shows supply-chain management is among the least effective AI applications, undermining rather than supporting the supply forecasting claim.

## Repository Structure

```
├── 📁 results/
│   ├── 📁 final/           # Kenya+Nigeria experiment results
│   └── 📁 archived/        # Historical results
├── 📁 predictive_results/  # Supply forecasting experiment results
├── 📁 stats/
│   ├── 📁 final/           # Statistical summaries
├── 📁 scripts/
│   ├── summarize_test.py          # Kenya+Nigeria experiment
│   ├── predictive_models/         # Supply forecasting experiment
│   │   ├── run_predictive_test.py # Main test script
│   │   └── analyze_predictive_results.py # Analysis
│   ├── analyze_results.py         # Statistical analysis
│   └── diff_stats.py             # Comparison utilities
├── 📁 source_materials/
│   ├── audere-whitepaper.md       # Audere sponsor white paper
│   ├── eprep-source.md            # PATH ePrEP guide (cited)
│   ├── ciz1096.pdf                # Balzer et al. paper (cited)
│   └── paper-in-question.md       # Original Lancet Comment
├── 📁 docs/
│   ├── hallucination_report.md          # Kenya+Nigeria analysis
│   ├── hallucination_supply_forecast.md # Supply forecasting analysis
│   └── investigation_log.md              # Investigation timeline
└── requirements.txt                      # Python dependencies
```

## Quick Start

### Prerequisites
- Python 3.7+
- OpenAI API key

### Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd kenya-nigeria-prep-hallucination-audit

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up OpenAI API key
export OPENAI_API_KEY="sk-your-key-here"
# Or create a .env file with: OPENAI_API_KEY=sk-your-key-here
```

### Running Experiments

#### Kenya + Nigeria Experiment
```bash
# Run with GPT-4o (10 seeds)
python scripts/summarize_test.py --seeds 10 --model gpt-4o-2024-11-20

# Analyze results
python scripts/analyze_results.py results/final/results_*.csv
```

#### Supply Forecasting Experiment
```bash
# Test with cited source (Balzer et al.)
python scripts/predictive_models/run_predictive_test.py --seeds 10 --model gpt-4o-2024-11-20 --prompt-type short

# Test with uncited source (Audere)
python scripts/predictive_models/run_predictive_test.py --src-file source_materials/audere-whitepaper.md --seeds 10 --model gpt-4o-2024-11-20 --prompt-type short

# Test without source (control)
python scripts/predictive_models/run_predictive_test.py --no-source --seeds 10 --model gpt-4o-2024-11-20 --prompt-type short

# Analyze results
python scripts/predictive_models/analyze_predictive_results.py
```

## Documentation

- **[Kenya+Nigeria Analysis](docs/hallucination_report.md)** - Original experiment findings
- **[Supply Forecasting Analysis](docs/hallucination_supply_forecast.md)** - Second experiment findings  
- **[Investigation Log](docs/investigation_log.md)** - Transparent timeline of investigation
- **[Source Materials](source_materials/)** - All original documents

## Reproducibility

All experiments are fully reproducible with:
- Deterministic seeds logged
- Complete prompt texts preserved  
- Timestamped outputs
- Model versions specified
- Dependencies pinned in requirements.txt

Both experiments provide empirical evidence suggesting that the disputed sentences in the published Comment may have originated from the Audere sponsor document rather than from the cited academic sources.
