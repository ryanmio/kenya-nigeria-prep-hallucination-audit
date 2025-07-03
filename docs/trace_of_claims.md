WORK IN PROGRESS

This document traces the claims in the Lancet HIV Comment to their source materials and evaluates the evidence for each claim, as well as the evidence of AI involvment and ultimately error.

---

## Claim 1: "In Kenya and Nigeria, AI powers telemedicine-based PrEP services that eliminate the need for frequent clinic visits."

### 1. Lancet Comment
The claim in the Lancet Comment is:
> In Kenya and Nigeria, AI powers telemedicine-based PrEP services that eliminate the need for frequent clinic visits.

### 2. Audere White Paper
The Audere white paper includes the following sentences which are relevant to the claim:

> Innovative approaches underway
> In low- and middle-income countries (LMICs), AI and telemedicine are transforming how HIV prevention—particularly PrEP—is delivered to those who need it most.

> Telemedicine has also opened new doors for PrEP access by eliminating the need for frequent in-person visits. In countries like Nigeria and Kenya, clients can start and manage PrEP through video consultations, app-based self-screening, and pharmacy pick-up options.

The Audere white paper does not cite any references for these claims, so we cannot evaluate the chain of evidence beyond the Audere white paper with any confidence.

Critically, the passage that contains both of these claims is flagged by GPTzero, a popular tool for detecting AI-written text, as likely AI-written. It assigned a probability of 100% to the passage. You can run the same test on the passage [here](https://app.gptzero.me/documents/90b7593e-7f65-4db7-9883-49f4ba3d059a/share). The author of the white paper is the same as the author of the Lancet Comment, so it seems reasonable to assume AI was used during the writing of the Comment, even if the final wording was not outright AI generated. This could be a case where the author used AI to gather information and then wrote the Comment by hand, but included errors propagated by the AI.

Further, the white paper includes several references that are seriously misrepresentative of the claims, and some outright contradict the claims entirely. Given the white paper is not peer-reviewed, we do not evaluate the merit of the claims versus the references in this repo, but we do view these erroneous references as evidence that the author of the white paper and Comment does not always carefully review the references they cite.

Given the white paper does not cite any references for the claim that AI powers telemedicine-based PrEP services in Nigeria, we cannot be certain where the claim originated. Further, we could not find any evidence of AI-powered telemedicine-based PrEP services in Nigeria during a cursory web search. Given the specificity of the claim, it seems unlikey the authors would have pulled it out of thin air, and AI misinterpretation somewhere in the chain of information seems more likely.

---

## Claim 2: "Predictive models could further enhance these programmes by helping providers identify individuals at greatest risk of HIV acquisition, forecast supply needs, and target outreach efforts more effectively."

### 1. Lancet Comment
The claim in the Lancet Comment is:
> Predictive models could further enhance these programmes by helping providers identify individuals at greatest risk of HIV acquisition, forecast supply needs, and target outreach efforts more effectively.

> At the systems level, AI could enable efficient resource planning and better decision making. Programme managers can analyse large-scale datasets to forecast medication stock, generate culturally tailored advice, identify geographical hotspots, improve outreach approaches, and refine training and resource allocation.

The Lancet Comment does not cite the Audere white paper for this claim, and instead cites Balzer et al's *Machine learning to identify persons at high-risk of human immunodeficiency virus acquisition in rural Kenya and Uganda.* However, the claim appears to lift exact text from the Audere white paper, as discussed below.

### 2. Audere White Paper
[Artificial intelligence to enhance HIV prevention in age of disruptions](https://static1.squarespace.com/static/64ff6a6dd00b77132a60f99b/t/681ccce37331774ae0b52d42/1746717923752/Leveraging+AI+to+enhance+HIV+prevention.pdf)

The Audere white paper includes the following sentences which are relevant to the claim:

> AI is further used to forecast medication demand, reducing stockouts and ensuring a stable supply of PrEP at decentralized locations.

> On a systems level, AI can contribute to data-informed decision-making through rapid analysis of large-scale datasets, including better forecasting of supply needs, optimizing outreach, and identifying geographic hotspots for intervention. 

Notably, it appears the Lancet Comment's text is lifted from the Audere white paper, with the following changes:
- "On a systems level" is changed to "At the systems level"
- "AI can contribute to data-informed decision-making" is changed to "AI could enable efficient resource planning and better decision making"
- "analysis of large-scale datasets" is changed to "analyse large-scale datasets"
- "forecasting of supply needs" is changed to "forecast medication stock"
- "optimizing outreach" is changed to "improve outreach approaches"
- "identifying geographic hotspots for intervention" is changed to "identify geographical hotspots"

The Audere white paper also combines multiple separate McKinsey white papers into one citation. The citation reads:
> McKinsey Global Institute. The Future of AI in Healthcare. McKinsey & Company; 2023. Available from: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-in-2023-generative-ais-breakout-year

The title of the citation is "The Future of AI in Healthcare", however the citation hyperlinks to "The state of AI in 2023: Generative AI’s breakout year". Further, we can find no evidence of a McKinsey Global Institute report titled "The Future of AI in Healthcare", although we found a LinkedIn and blog post that repeat this same citation, both of which appear entirely AI-generated. This is a telltale sign of AI hallucination.

- LinkedIn post: https://www.linkedin.com/pulse/future-ai-healthcare-trends-predictions-piyush-david-1ikjc/
- GPTzero analysis showing 100% AI-generated: https://app.gptzero.me/documents/10bc721f-5fb6-4009-a36c-5fd5334293dd/share

- Blog post: https://www.numberanalytics.com/blog/ai-revolution-healthcare-pharma-next5years
- GPTzero analysis showing 100% AI-generated: https://app.gptzero.me/documents/a0e7ae9d-6994-46c9-b2a1-a0ff24c67902/share

Could it be a coincidence that the author of the Audere white paper cited the same McKinsey report as two 100% AI-generated posts? Sure, but it seems highly unlikely.

More likely is that the author replied upon an AI-generated citation that does not exist, as did the authors of the LinkedIn post and blog post. AI tools such as Deep Research are well-known to hallucinate citations.

Let's pretend for a moment that the Audere white paper made an error in either the title of the citation or the URL. Given the URL is more specific, we will evaluate the McKinsey State of AI in 2023 report and continue to trace the claim from there.

### 3. McKinsey State of AI in 2023
The state of AI in 2023: Generative AI’s breakout year https://mck.co/3YdJbED

The McKinsey white paper provides two graphs showing AI-driven cost decreases and revenue increases across business functions. Contrary to the Audere claim, supply chain management scores worst in both categories. ![McKinsey AI value by function](../source_materials/McKinsey-screenshot.png)

Thus, not only is the Comment's claim unsupported by the Audere white paper, it is also contradicted by the McKinsey white paper.

Further, the McKinsey white paper does not include any evidence for the claim that AI could enable optimized outreach or identify geographical hotspots for intervention.