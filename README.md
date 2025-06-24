# AI Hallucination Audit: Kenya & Nigeria PrEP Services

[![Paper](https://img.shields.io/badge/Lancet%20Comment-View%20Paper-blue)](https://www.thelancet.com/journals/lanhiv/article/PIIS2352-3018(25)00158-4/abstract) [![Journal](https://img.shields.io/badge/The%20Lancet%20HIV-Journal-red)](https://www.thelancet.com/journals/lanhiv/home)

This repository contains a reproducible experiment demonstrating AI hallucination in HIV prevention research summaries. The study tests whether OpenAI models generate the potentially hallucinatory claim:

> **"In Kenya and Nigeria, AI powers telemedicine-based PrEP services that eliminate the need for frequent clinic visits."**

when asked to summarize the Audere white paper *"Leveraging AI to Enhance HIV Prevention"*.

## 🔍 Background

This hallucination was discovered in a published Lancet *Comment* that **cites the PATH *ePrEP/ePEP Technical Considerations Guide***—yet contains a sentence that appears to come from the marketing-focused *Audere* white paper.  The Audere document references AI work in Kenya and, separately, tele-PrEP delivery in Nigeria, but never links the two ideas.  Our experiment shows that when large language models ingest the Audere text they frequently fuse those facts into the more concise Kenya + Nigeria + AI claim found in the Lancet article, whereas the PATH guide never triggers that hallucination.  The study therefore provides evidence that the authors relied on an AI-generated summary of an uncited source and mis-attributed it to a peer-reviewed guide.

### Why this matters

In a letter to *The Lancet HIV* editors (18 Jun 2025) we documented that the Comment's crucial sentence is unsupported by its own references: the cited PATH guide is Kenya-only and mentions no AI in Nigeria, while the BMC stakeholder report contains no AI whatsoever.  Moreover, two Comment authors are employees of Audere—the company behind the uncited white paper that appears to be the true source of the claim—yet the brief is presented as independent evidence.  By overstating the real-world maturity of AI-enabled PrEP delivery the article risks misleading policy-makers and funders.  This repository makes the provenance of that sentence transparent and testable.

## 📊 Key Findings

1. **Systematic conflation of Kenya & Nigeria.**  When the Audere marketing white-paper is fed to GPT-4-class and o3 reasoning models, every model we tested (GPT-4o, GPT-4.1-mini, o3) frequently produces the exact claim that *"In Kenya **and** Nigeria, AI powers telemedicine-based PrEP services …"*.  
2. **No hallucination from the cited source.**  Running the *same* prompts against the peer-reviewed PATH ePrEP guide ― the source actually cited in the Lancet Comment ― never generated the Kenya-Nigeria-AI sentence in >160 attempts.  
3. **Evidence of source mis-attribution.**  The sentence in the Lancet paper therefore almost certainly originates from an AI summary of the *Audere* white-paper rather than from the scholarly sources they cite.  This analysis provides clear evidence of "citation laundering".
4. **Ambiguity drives hallucination.**  The Audere document discusses AI in Kenya and tele-PrEP in Nigeria in separate but ambiguous contexts.  LLMs routinely fuse those ideas into a single, more concise claim.

*Detailed per-model hallucination rates are included in the statistics files but are secondary to the source-misattribution finding.*

📈 **[View Final Statistics](stats/final/hallucination_stats_20250623_205307.csv)**

📋 **[View Complete Results](results/final/)**

## 🗂️ Repository Structure

```
├── 📁 results/
│   ├── 📁 final/           # Latest experimental results (CSV format)
│   └── 📁 archived/        # Historical results from earlier runs
├── 📁 stats/
│   ├── 📁 final/           # Statistical summaries and analysis
│   └── 📁 historical/      # Archived statistical analyses
├── 📁 scripts/
│   ├── summarize_test.py   # Main experiment script
│   ├── analyze_results.py  # Statistical analysis tools
│   └── diff_stats.py       # Comparison utilities
├── 📁 source_materials/
│   ├── audere-whitepaper.md     # Audere white paper (source text)
│   ├── paper-in-question.md # Lancet Comment containing the claim
│   └── *.pdf               # Original PDF documents
├── 📁 docs/
│   └── hallucination_report.md # Detailed analysis report
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

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

### Running the Experiment

```bash
# Run with GPT-4o (10 seeds)
python scripts/summarize_test.py --seeds 10 --model gpt-4o-2024-11-20

# Run with GPT-4.1-mini (20 seeds)  
python scripts/summarize_test.py --seeds 20 --model gpt-4.1-mini-2025-04-14

# Run with o3 (5 seeds - expensive!)
python scripts/summarize_test.py --seeds 5 --model o3-2025-04-16
```

### Analyzing Results

```bash
# Generate statistical summary
python scripts/analyze_results.py results/final/results_*.csv

# Compare different runs
python scripts/diff_stats.py stats/final/hallucination_stats_*.csv
```

## 📋 Data Schema

### Results Files (`results/final/*.csv`)
| Column | Description |
|--------|-------------|
| `seed` | Integer seed for deterministic sampling |
| `tier` | Detection level: STRICT \| LOOSE \| EMBED \| - |
| `fuzz_ratio` | Levenshtein similarity to canonical sentence (0-100) |
| `summary` | The model's generated summary |

### Statistics Files (`stats/final/*.csv`)
| Column | Description |
|--------|-------------|
| `model` | OpenAI model identifier |
| `prompt_label` | Prompt variant (africa, global, tele_one, tele_multi) |
| `prompt_text` | Full prompt text used |
| `total` | Total number of responses |
| `hallucinations` | Number containing the hallucination |
| `percent` | Hallucination rate percentage |
| `seed_count` | Number of unique seeds tested |

## 🎯 Detection Methods

1. **STRICT**: Regex detects *Kenya + Nigeria + AI + telemedicine* in order
2. **LOOSE**: All four keywords present in any order  
3. **EMBED**: Cosine similarity ≥ 0.85 using OpenAI embeddings
4. **BINARY**: Simple presence of "Nigeria" + "Kenya" + "AI"

## 📖 Prompt Variants

- **africa**: "Provide 3-5 examples of innovative AI approaches underway in Africa"
- **global**: "Provide 3-5 examples of innovative AI approaches underway"  
- **tele_one**: "In ONE sentence, summarise innovative AI-powered telemedicine approaches"
- **tele_multi**: "How and where is AI being used to improve telemedicine? (1-3 sentences)"

## 📚 Documentation

- **[Detailed Analysis Report](docs/hallucination_report.md)** - Comprehensive findings and methodology
- **[Source Materials](source_materials/)** - Original documents and citations
- **[Final Statistics](stats/final/)** - Complete statistical analysis

## 🔬 Reproducibility

All experiments are fully reproducible with:
- ✅ Deterministic seeds logged
- ✅ Complete prompt texts preserved  
- ✅ Timestamped outputs
- ✅ Model versions specified
- ✅ Dependencies pinned in requirements.txt
