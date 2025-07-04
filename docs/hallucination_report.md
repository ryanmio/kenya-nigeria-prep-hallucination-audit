# AI-Generated Kenya + Nigeria Tele-PrEP Claim: Hallucination Audit

Paper: https://www.thelancet.com/journals/lanhiv/article/PIIS2352-3018(25)00158-4/abstract

## Hypothesis

A sentence in the Lancet Comment — *"In Kenya and Nigeria, AI powers telemedicine-based PrEP services that eliminate the need for frequent clinic visits."* — is the result of LLM hallucination.  
Specifically, we suspect the authors relied on an AI summary of the Audere white-paper rather than on the two peer-reviewed sources they cite. If true, running modern LLMs on the Audere report should frequently recreate the Kenya + Nigeria claim, whereas running the same prompts on one of the cited sources (PATH ePrEP guide) should not.

## Methodology

Our investigation followed a three-phase workflow that can be fully reproduced from the code in this repository.

**1. Preparing the source texts.**  We began by converting the primary marketing document, `audere-whitepaper.pdf`, and the peer-reviewed comparator, `ePrEP-ePEP-technical-considerations-guide-PATH-2024.pdf`, into UTF-8 Markdown (`audere-whitepaper.md` and `eprep-source.md`).  Converting to plain text ensures the models receive the exact same content we reviewed and removes any biases that might be introduced by PDF rendering quirks.

**2. Querying the language models.**  Using `scripts/summarize_test.py` we passed the entire Markdown text to three OpenAI chat models—`gpt-4o-2024-11-20`, `gpt-4.1-mini-2025-04-14`, and `o3-2025-04-16`.  Each run was preceded by the grounding instruction *"You are an experienced scientific writer. Base your answer ONLY on the user-supplied text…"* and one of four prompt variants that stress different information needs (summaries focused on Africa, on global telemedicine, on a single tele-PrEP example, or on multiple telemedicine use cases).  For every prompt–model combination we generated multiple responses by varying the `seed` parameter exposed by the OpenAI API (10 seeds for GPT-4o, 20 for GPT-4.1-mini, 5 for o3).  Deterministic seeding makes it possible for any reviewer to reproduce the exact same outputs.

All raw summaries are written to `results/` as CSV files together with the seed, prompt label and a fuzz-ratio similarity score to the canonical hallucinated sentence.

**3. Detecting hallucinations and analysing results.**  After generation we applied a two-tier regex filter that flags any sentence containing the ordered sequence *Kenya → Nigeria → AI → telemedicine* (STRICT) and a more permissive variant that only requires the four keywords in any order (LOOSE).  Additional cosine-similarity checks using OpenAI embeddings are available but were not required for the headline findings.  The helper script `scripts/analyze_results.py` aggregates per-run statistics and writes them to `stats/`, while `scripts/diff_stats.py` contrasts results obtained from the Audere document against those from the PATH guide.

Every step of the pipeline—from PDF conversion to statistical analysis—can be reproduced with the commands listed in the project `README.md`.  Dependencies are pinned in `requirements.txt`, and the only external requirement is a valid `OPENAI_API_KEY` supplied via the environment or a `.env` file.

## Results

### Audere Report (`audere-whitepaper.md`)

| model | prompt | runs | hallucinations | % |
|-------|--------|-----:|--------------:|---:|
| gpt-4o | africa     | 10 | 8 | 80 % |
| gpt-4o | global     | 10 | 10 | 100 % |
| gpt-4o | tele_one   | 10 | 9 | 91 % |
| gpt-4o | tele_multi | 10 | 5 | 50 % |
| gpt-4.1-mini | africa     | 20 | 20 | 100 % |
| gpt-4.1-mini | global     | 20 | 20 | 100 % |
| gpt-4.1-mini | tele_one   | 20 | 20 | 100 % |
| gpt-4.1-mini | tele_multi | 20 | 16 | 80 % |
| o3 | africa     | 1 | 1 | 100 % |
| o3 | global     | 1 | 1 | 100 % |
| o3 | tele_one   | 2 | 1 | 50 % |
| o3 | tele_multi | 2 | 2 | 100 % |

### PATH ePrEP Guide (`eprep-source.md`)

| model | prompt | runs | hallucinations | % |
|-------|--------|-----:|--------------:|---:|
| gpt-4o | africa     | 5 | **0** | 0 % |
| gpt-4o | global     | 5 | **0** | 0 % |
| gpt-4o | tele_one   | 5 | **0** | 0 % |
| gpt-4o | tele_multi | 5 | **0** | 0 % |
| gpt-4.1-mini | africa     | 5 | **0** | 0 % |
| gpt-4.1-mini | global     | 5 | **0** | 0 % |
| gpt-4.1-mini | tele_one   | 5 | **0** | 0 % |
| gpt-4.1-mini | tele_multi | 5 | **0** | 0 % |
| o3 | africa     | 0 | **0** | 0 % |
| o3 | global     | 0 | **0** | 0 % |
| o3 | tele_one   | 0 | **0** | 0 % |
| o3 | tele_multi | 0 | **0** | 0 % |

## Conclusion

LLMs frequently hallucinate the claim that **AI-powered telemedicine PrEP exists in both Kenya *and* Nigeria** when summarising the Audere report, but **never do so** when summarising the peer-reviewed PATH ePrEP guide cited in the paper.
These results suggest that the sentence in the Lancet Comment may have come from an AI-generated summary of the Audere marketing paper rather than from the cited scientific sources.

The full pipeline (code, prompts, seeds, raw summaries, statistics) is available in this repository for independent verification.
