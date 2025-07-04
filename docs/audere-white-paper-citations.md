# Audit of Questionable Citations in the Audere White-Paper

> **Scope**  This note investigates five references in the Audere consultation white-paper that exhibit the hallmark patterns of AI-generated or otherwise erroneous citations.  Each entry documents what the citation claims to point to, what we actually found, and why the discrepancy matters.

---

## Citation 10: McKinsey Global Institute – Fabricated "Frankenstein" Citation

**What the white-paper cites:**
```
McKinsey Global Institute. The Future of AI in Healthcare. McKinsey & Company; 2023. Available from: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-in-2023-generative-ais-breakout-year
```

**The issue:** This citation appears to be a fabricated hybrid that combines a non-existent report title with a URL to a different McKinsey publication.

**Evidence:**
1. Extensive searches of McKinsey.com, Google Scholar, and web archives return zero results for any McKinsey Global Institute report titled "The Future of AI in Healthcare."
2. The provided link leads to "The state of AI in 2023: Generative AI's breakout year" – a general AI survey with no healthcare focus.
3. Two external sources (a LinkedIn post and blog article) reproduce this exact same title-URL mismatch; GPTZero analysis indicates both are 100% AI-generated content.

**Uncertainty:** While we cannot definitively prove the citation was AI-generated, the pattern strongly suggests automated reference creation without human verification.

---

## Citation 17: The Global Fund – Unverifiable Strategy Document

**What the white-paper cites:**
```
The Global Fund. Strategy to Integrate Digital Health and AI in Global Fund Programs. Geneva: The Global Fund; 2023.
```

**The issue:** This strategy document appears to not exist in any publicly accessible form.

**Evidence:**
1. **Institutional search:** No document with this title appears on the Global Fund website, board papers, or strategic initiative repositories.
2. **Archive verification:** Wayback Machine snapshots from 2023 contain no reference to such a strategy.
3. **Staff confirmation:** Two Global Fund staff members, contacted via publicly listed emails, confirmed they were "unaware of such a strategy document."

**Uncertainty:** The document could theoretically exist as an internal or unpublished report, though the absence of any public reference makes this unlikely.

---

## Citation 8: Gates Foundation – Non-existent Report with Broken Link

**What the white-paper cites:**
```
Bill & Melinda Gates Foundation. AI and Data Science in Global Health: Innovation and Opportunity. Gates Foundation; 2023. Available from: https://www.gatesfoundation.org/ideas/media-center/press-rleases/2023/08/grand-challenges-rfp-recipients-ai-large-language-models
```

**The issue:** No Gates Foundation report with this title exists, and the provided URL is broken.

**Evidence:**
1. **Title verification:** Searches of the Gates Foundation media center and broader web return zero hits for this exact title.
2. **Broken link:** The URL returns 404 error (note misspelling: "press-rleases").
3. **Closest match:** The URL appears to reference a 2023 RFP announcement, but this is neither a report nor matches the cited title.

**Uncertainty:** This could represent a transcription error of an actual Gates Foundation document, though extensive searching has not located any plausible alternative.

---

## Citations 6 & 7: Valid Articles with Irrelevant Appended Links

**What the white-paper cites:**

Citation 6:
```
Fahey, Carolyn A., et al. "Machine Learning with Routine Electronic Medical Record Data to Identify People at High Risk of Disengagement from HIV Care in Tanzania." PLOS Global Public Health, vol. 2,no. 9, 16 Sept. 2022, e0000720. https://doi.org/10.1371/journal.pgph.0000720. https://www.who.int/news/item/06-03-2025-who-announces-new-collaborating-centre-on-ai-for-health-governance
```

Citation 7:
```
Ma, Yuanchao et al. "The first AI-based Chatbot to promote HIV self-management: A mixed methods usability study." HIV medicine vol. 26,2 (2025): 184-206. doi:10.1111/hiv.13720 https://www.who.int/news/item/06-03-2025-who-announces-new-collaborating-centre-on-ai-for-health-governance
```

**The issue:** Both citations append an unrelated WHO press release URL to otherwise valid journal article references.

**Evidence:**
1. **Primary citations valid:** Both journal articles exist and are accessible via their DOIs.
2. **Secondary links irrelevant:** The WHO URL (identical in both citations) leads to a March 2025 press release about an AI governance center, completely unrelated to either study.
3. **Pattern suggests automation:** The identical irrelevant URL in both citations indicates systematic rather than random error.

**Uncertainty:** This could result from copy-paste errors, citation management software malfunction, or AI-assisted reference compilation without adequate human review.

---

## Implications for Scientific Integrity

These citation errors demonstrate patterns consistent with AI-generated references that lack human verification. The combination of non-existent documents, URL mismatches, and duplicate irrelevant links suggests the use of automated tools without adequate quality control.

**Potential consequences:**
- Undermines confidence in the white-paper's evidence base
- Risk of error propagation to downstream publications
- Misrepresentation of institutional positions (McKinsey, Gates Foundation, Global Fund)

**Limitations of this analysis:**
- We cannot definitively prove AI involvement without access to the authors' workflow
- Some documents could theoretically exist in non-public forms
- Citation errors could result from other causes including human transcription mistakes

**Recommendations:**
1. Authors should verify all citations independently before publication
2. AI-assisted reference generation requires mandatory human cross-checking
3. Corrections should be issued for demonstrably false citations

---

*Analysis conducted July 2025 following reproducible methodology documented in the kenya-nigeria-prep-hallucination-audit repository*
