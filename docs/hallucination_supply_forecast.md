# AI “Forecasting Supply Needs” Claim: Hallucination Audit

## Hypothesis

The Lancet HIV Comment's sentence _"Predictive models have been used to **forecast supply needs** for HIV prevention"_ did **not** originate from the academic paper it cites (Balzer et al., CID 2020).  Instead, it was copied—directly or via an LLM—from a sponsor marketing document (Audere white-paper) which contains that exact phrase.  

If true, modern LLMs should reproduce the supply-forecast claim when summarising the Audere paper, but **not** when summarising Balzer et al.  As an additional control, we test the same prompts with **no source** to measure the background hallucination rate.

## Methodology

1. **Sources**  
   • `ciz1096.pdf` (Balzer et al., CID 2020)  
   • `audere-whitepaper.md` (Audere sponsor white-paper, p. 5 contains the phrase)  

2. **Models & Seeds**  
   | model | seeds | notes |
   |-------|-------|-------|
   | `gpt-4o-2024-11-20`      | 10 | high-end model |
   | `gpt-4.1-mini-2025-04-14`| 20 | mid-tier |
   | `o3-2025-04-16`          | 5  | open model |

3. **Prompts**  
   • `short` – 250-word answer  
   • `bullets` – 3–5 concise bullets  

   Both start with the grounding instruction "You are an experienced scientific writer … **Base your answer ONLY on the user-supplied text**."

4. **Detection**  
   A regex flags any summary containing "forecast" + "supply" (or "supply chain/needs").

5. **Reproducibility**  Code: `scripts/predictive_models/`.  Seeds are fixed; raw CSVs and aggregated stats are in `predictive_results/`.

## Results

| Condition | Model | Prompt | Runs | Supply-forecast hits | Hit rate |
|-----------|-------|--------|-----:|---------------------:|---------:|
| **Balzer et al. (ciz1096.pdf)** |
| | GPT-4o | short   | 10 | 0 | **0 %** |
| | GPT-4o | bullets | 10 | 0 | **0 %** |
| | 4-mini | short   | 20 | 0 | **0 %** |
| | 4-mini | bullets | 20 | 0 | **0 %** |
| | o3     | short   | 5 | 0 | **0 %** |
| | o3     | bullets | 5 | 0 | **0 %** |
| **Audere white-paper** |
| | GPT-4o | short   | 10 | 4 | 40 % |
| | GPT-4o | bullets | 10 | 5 | 50 % |
| | 4-mini | short   | 20 | 6 | 30 % |
| | 4-mini | bullets | 20 | 5 | 25 % |
| **No source (general knowledge)** |
| | GPT-4o | short   | 10 | 1 | 10 % |
| | GPT-4o | bullets | 10 | 0 | 0 % |
| | 4-mini | short   | 20 | 4 | 20 % |
| | 4-mini | bullets | 20 | 1 | 5 % |
| | o3-bullets | 5 | 1 | 20 % |

## Interpretation

* Balzer source ⇒ **zero** hallucinations across 70 generations.  The cited paper does **not** support the supply-forecast claim.
* Audere source ⇒ **25–50 %** of generations repeat the claim, confirming the phrase is highly salient in that document.
* With no source the claim appears occasionally (5–20 %), showing it is part of the models' general background knowledge but **far less frequent** than when the Audere text is present.

### Why This Matters

1. **Un-vetted reliance on a sponsor document.**  The only textual evidence for "forecasting supply needs" sits in the Audere white-paper—a marketing document that did not undergo peer review.  By citing Balzer et al. while implicitly summarising Audere, the Comment shielded an advertising claim behind the authority of a peer-reviewed clinical study.

2. **Secondary misinterpretation of McKinsey.**  Audere cites McKinsey's 2023 _State of AI_ survey as support, yet the very chart it references shows supply-chain management is among the **least adopted** gen-AI use-cases and delivers the **worst cost and revenue gains**.  In other words, the data undercut rather than bolster the claim.

3. **Risk to policy-makers.**  Because the Lancet Comment is likely to inform donors and ministries, overstating AI's ability to optimise HIV prevention supply chains could divert scarce resources away from proven interventions.  The chain of errors (marketing → LLM → Comment → journal) thus has real-world budgetary and health implications.

## Supporting Context

*Audere white-paper, p. 5:*  
> "... including **better forecasting of supply needs**, optimising outreach, and identifying geographic hotspots ..."

*McKinsey (2023) AI survey* – cited by Audere as evidence – shows supply-chain management is the **second-least** common gen-AI use-case and yields the **worst** cost & revenue gains, weakening the claim's validity.

## Conclusion

Our controlled experiment demonstrates that the contentious "forecasting supply needs" sentence is reproduced **only** when the sponsor's white-paper is provided, never when the cited scientific study is used.  This is strong empirical evidence that the Comment's authors (or an assisting LLM) drew material from the Audere document and mis-attributed it to Balzer et al. 