# Investigation Log: Kenya-Nigeria Tele-PrEP Claim Analysis

> **Purpose**: This log documents my thought process during this investigation, including uncertainties, corrections, and evolving understanding. It is not meant as definitive claims, but as a transparent record of open inquiry.

---

## Entry 1: June 16, 2025 - Article Forwarded & Initial Reaction

My father's partner, who worked in AIDS research her entire career, forwarded me a Lancet HIV Comment about AI in HIV prevention. She knows I'm interested in AI in medicine and sent it with no comment - just sharing something she thought I'd find interesting. My immediate response was highly skeptical about the AI proposals. But upon closer inspection, I noticed what appeared to be concerning discrepancies: the citations didn't seem to match the claims being made. The Kenya/Nigeria AI telemedicine claim cited sources that, to my reading, didn't actually support it, and several other citations seemed potentially misrepresented as well. 

As I examined more citations, I began to worry there might be a broader pattern. For example, Citation 8 appeared to support claims about "AI chatbots, SMS reminders, and virtual self-risk assessments" offering "greater privacy, convenience, and autonomy," but the cited study seemed to evaluate only a single Montreal chatbot with 28 participants, contained no SMS component or virtual self-risk assessment, and had no comparison group to support claims about "greater" anything. 

What concerned me most was the potential real-world impact: overstating the maturity of AI-enabled PrEP delivery could mislead policy-makers and funders, potentially diverting scarce HIV prevention resources toward unvalidated technologies rather than proven interventions. Given the stakes involved in HIV prevention, I felt these discrepancies warranted closer examination. I want to acknowledge upfront that I may be misunderstanding the authors' intent or missing context that would clarify these apparent inconsistencies.

---

## Entry 2: June 17, 2025 - Direct Engagement on LinkedIn

I decided to try engaging directly with the author by commenting on their LinkedIn post promoting the paper. I wanted to give them an opportunity to clarify what appeared to be discrepancies before taking any other steps. My comment raised concerns about potential overstatement of AI capabilities and cited specific examples where the claims didn't seem to match the sources, while asking if they could clarify these points. I tried to frame this constructively, focusing on the potential impact on HIV prevention resources, though I recognize my tone may have come across as more confrontational than I intended. The author did not respond to the comment.

Here's the comment I sent:
> "Do you think your paper could unintentionally set back HIV prevention by overstating the current capabilities of AI tools? Several claims don't seem to match your cited sources, and I worry this might misdirect limited resources away from proven interventions.
> 
> For example, you write "In Kenya and Nigeria, AI powers telemedicine-based PrEP services that eliminate the need for frequent clinic visits." ⁵ ⁶, but Ref 6 only describes a small Kenyan pilot where AI assists with photo quality checking of HIV self-tests—it doesn't "power" the telemedicine services, doesn't eliminate clinical oversight, and doesn't mention Nigeria at all. Notably, this AI system was built by Audere, your own sponsor, yet you're citing it as independent evidence while overstating its capabilities. Ref 5 is a Nigerian workshop on pharmacy-based PrEP design with no AI involved.
> 
> Your paper draws its key recommendations (Ref 3) from a brief published by Audere, your own sponsor, which appears to be promotional material rather than actual research. This is exactly the type of AI hype that risks misdirecting HIV prevention resources toward unproven technologies rather than evidence-based interventions.
> 
> Given the high stakes in HIV prevention, could you clarify these discrepancies?"

The comment was deleted by the lead author, Jirair Ratevosian.

---

## Entry 3: June 18, 2025 - Contacting The Lancet HIV

After my LinkedIn comment went unanswered, I decided to respectfully contact the journal to seek clarification about what appeared to be citation discrepancies. I raised three concerns that I hoped the authors could help clarify: what seemed to be misrepresentation of cited evidence for the Kenya/Nigeria claim, the use of sponsor material as independent evidence, and apparent scope misrepresentation in other citations. I emphasized that my goal was simply to ensure accuracy in the scientific record and that I was open to correction if I had misunderstood something. Peter Hayward responded quickly with acknowledgment that they would look into it.

---

## Entry 4: June 23, 2025 - Developing LLM Analysis

I decided to develop additional evidence to better understand the potential source of the discrepancy and created this GitHub repository with LLM reproduction tests to explore how the claim might have originated from AI summarization of the Audere whitepaper. The findings were intriguing, though I recognize they are not definitive proof: LLMs consistently produce the Kenya + Nigeria + AI claim when summarizing the Audere document, but never when summarizing the cited PATH guide. While this suggests a possible explanation for the citation mismatch, I acknowledge there could be other explanations I haven't considered. I shared this analysis with the journal, and they said they were seeking a response from the authors and would get back to me by the end of the week.

---

## Entry 5: June 25, 2025 - Author Blocks Me, Contacting Duke Integrity Office

After my LinkedIn comment went unanswered, I later discovered that the lead author, Jirair Ratevosian, had blocked me from viewing their profile before deleting my comment. I understand that researchers may receive unwanted contacts and may have reasons for limiting interactions, but this response left me unable to seek direct clarification that might have resolved my concerns. Given the potential research integrity implications and my inability to engage directly with the author, I reluctantly decided to contact Duke University's Office of Scientific Integrity, emphasizing that I hoped this could lead to clarification rather than conflict. Dr. Donna Kessler acknowledged that my concerns would be reviewed under applicable policies.

---

## Entry 6: June 29, 2025 - Expanding the Investigation

The journal said they hoped to have a response by June 27, but there's been no word yet despite my follow-up. Duke is reviewing under their policies, and the author has blocked direct communication. I believe my analysis suggests a possible explanation for the citation discrepancy - that the sentence may have originated from AI summarization of sponsor materials rather than cited sources - but I remain open to alternative explanations that I may not have considered.
Today I also spent some time reading other papers and commentary pieces by the lead author, Jirair Ratevosian. Using the same cautious approach, I compared several headline claims with their cited references and, in multiple cases, could not find support for the statements. I have begun documenting those examples in the [pattern folder](/docs/pattern/) of this repository so that any reviewer can check my reading. This early scan strengthens my sense that the original issue may not be isolated, though I still acknowledge the possibility that I have missed context or misunderstood the authors' intent.

I also re-ran the workflow on a second disputed sentence: *"Predictive models could further enhance these programmes by helping providers identify individuals at greatest risk of HIV acquisition, forecast supply needs, and target outreach efforts more effectively.7"*  In this sentence, the first and last clauses align with Balzer et al., but the **"forecast supply needs"** clause does not appear in that study.  When the LLMs were forced to base their answer on Balzer et al., supply-forecast language never appeared (0 % hit-rate).  When supplied with the Audere sponsor white-paper, however, the same models repeated the phrase in 25–50 % of generations—mirroring what ended up in the Comment.  The white-paper itself cites McKinsey's 2023 State of AI survey as evidence, yet that survey actually shows supply-chain management is one of the least common and least valuable AI use-cases.  In short, the claim rests on a chain of misinterpretation: McKinsey data → oversold in Audere marketing → copied by an LLM → published in the Comment and mis-cited to Balzer.  As a control, I also ran the prompts with *no source text at all*; supply-forecast wording appeared only occasionally (5–20 percent), confirming it is background knowledge for the models but far less likely to surface than when the Audere text is provided.

---

## Entry 7: June 30, 2025 - Update from the Journal

The journal responded this morning. Peter Hayward apologized for the delay and explained that, because this is the first time The Lancet HIV has encountered a case like this, he is consulting colleagues in the wider Lancet group and that due diligence is taking longer than expected. He hopes to have a full response by the end of the week. I acknowledged his update, thanked him for the ongoing review, and noted that this [one](https://github.com/ryanmio/kenya-nigeria-prep-hallucination-audit/blob/main/docs/pattern/citation7_staff_count_error.md) numerical typo could likely be addressed quickly without waiting for the broader investigation.

*This log will be updated as the investigation progresses. All entries reflect my thinking at the time of writing and may be revised based on new evidence.* 