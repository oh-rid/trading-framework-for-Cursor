### 📦 UNIVERSAL MERGE PROMPT (v2.3 · 2025-07-29)

*Combine **N** distillates (each in format **“Universal Distillation Prompt v4.4”**) into one master file.*

────────────────────────────────────────────────────────────
## 0 · Input format
Every source summary must follow v4.4 exactly:  
LLM-USAGE → Meta Layer → Principles → ConceptGraph → KeyFormulas →  
Glossary → Bias Glossary → Tag Legend → SourceMap

Special traits of v4.4:  
* `Principles` include **Flex** plus sub-lines `Tags:` and `Fails:`;  
* `Regime:` is optional;  
* `SourceMap` holds **Author, Title, Year, Type**.

────────────────────────────────────────────────────────────
## 1 · Merge rules (“engine room”)

| № | Action | Details |
|---|--------|---------|
| **1.1** | **Global numbering** | BI01 … M01 … P01 … F01 … T01 … B01 … |
| **1.2** | **Deduplication — semantics** | Detect duplicates by meaning (~80 % similarity). If unsure keep both, mark `⚠Possible dup`. |
| **1.3** | **Conf & Imp merge** | For duplicates use `Conf = max`, `Imp` = highest severity (C > M > m). |
| **1.4** | **Flex** | If any source has `Flex:Core` → result `Flex:Core`; else `Flex:Advisory`. |
| **1.5** | **Tags / Fails / Regime** | Merge `Tags:` and `Fails:` separately; total ≤ 6 codes. If QE vs QT conflict → add `⚠Conflict:` (≤ 10 words). Merge `Regime:` via OR; if none present do not create. |
| **1.6** | **Glossaries** | Drop duplicate T- and B-codes, sort A→Z. |
| **1.7** | **ConceptGraph** | Merge all triples; if > 50 lines keep top-50 by (in+out) degree. |
| **1.8** | **Sorting** | Principles: Foundation (M-category) → Tactic. Inside: `(Flex)` Core→Advisory, then `Imp` C→M→m, finally descending `Conf`. |
| **1.9** | **Token budget** | Output ≤ 7 000 tokens. If larger: ① cut `Imp=m` lines, list them in `#Tail:`; ② trim examples/quotes to ≤ 10 words. |
| **1.10** | **References** | All `Src:` → new global BI-codes; renumber F/T/B after dedup.

────────────────────────────────────────────────────────────
## 2 · Final output (exact order & format)

```markdown
### {PROJECT}_DISTILLATE v1.0

##### LLM-USAGE
- Treat rules as priors, not dogma.  
- You may override if new evidence ≥ Conf of prior.  
- Cite principle ID when disagreeing.  
- Bias-check before applying any rule.  
- Keep output ≤ 5 000 tokens.

---

#### Meta Layer
BigIdeas: BI01, BI02, …  
MetaPrinciples:
[M01] … | Conf:0.88 | Imp:C | Src:BI01
[M02] …  
KeyFormulas: F01, F02, …  
Glossary add: T01, T02, …

---

#### Principles
[P01] … | Works: … | Fails: … | Act: … | Conf:0.90 | Imp:C | **Flex:Core**  
| Tags: M=QE;C=EZ  
| Fails: M=QT  
| Regime: QE & GDP>0  
| Bias:B07 | Src:BI02  
…  
#Tail: P98 P99           <!-- if Imp=m lines pruned -->

---

#### ConceptGraph
Term → relation → Term  
…

---

#### KeyFormulas
[F01] … | Conf:0.80 | Imp:M | Src:BI03  
…

---

#### Glossary
[T01] Term = definition | Src:BI02  
…

---

#### Bias Glossary
[B01] Bias = explanation  
…

---

#### Tag Legend
| Cat | Codes  | Meaning             |
|-----|--------|---------------------|
| **M** | QE QT HR | Monetary regimes   |
| **C** | EZ TI     | Credit standards   |
| **I** | DI SI     | Inflation regimes  |
| **S** | UP OS     | Supply balance     |
| **R** | GR TX     | Regulation / Taxes |

`Tags:` — contexts where rule is valid. `Fails:` — contexts where effect breaks.

---

#### Impact Scale (Imp)
| Code | Meaning                                             |
|------|-----------------------------------------------------|
| **C** | Critical — failure = bankruptcy / portfolio crash   |
| **M** | Major    — ±200 bps ROI or volatility > 30 %        |
| **m** | Minor    — local, reversible effect < 200 bps       |

#### Confidence Scale (Conf)
| Range | Typical evidence                                   |
|-------|----------------------------------------------------|
| 0.90–1.00 | Meta-analysis, ≥ 3 datasets, p < 0.01           |
| 0.70–0.89 | Peer-review + ≥ 10 years data                   |
| 0.40–0.69 | Working paper, limited dataset                 |
| 0.10–0.39 | Author opinion / single case study             |

---

#### SourceMap
BI01 = «Author A., “Full Title”, 2024, book»  
BI02 = …  
…

#MERGE completed YYYY-MM-DD  
#META BigIdeas: BI01, BI02, …
```
────────────────────────────────────────────────────────────
<!-- ########################## INTERNAL STEPS (do NOT output) ##########################
1. **Load inputs** Read every v4.4 distillate file as a structured object (dict).
2. **Global counters** Initialise counters: BI=1, M=1, P=1, F=1, T=1, B=1.
3. **Entity loop** For each distillate, for each entity type (MetaPrinciple, Principle, …):  
   • Check existing text for 80 % similarity.  
   • If duplicate → merge following rules 1.2–1.5; update `Conf/Imp/Flex/Tags/Fails`.  
   • Else → assign next global code (e.g., new Principle → P{index:02d}).
4. **Tags/Fails sanity** Remove duplicates inside each list; truncate to 6 codes; add `⚠Conflict` if needed.
5. **ConceptGraph aggregation** Merge triples, count degree; retain top-50 if oversize.
6. **Glossary & Bias** Merge, deduplicate, A→Z sort; re-index T## / B##.
7. **SourceMap** For every distinct BI-code, ensure Author, Title, Year, Type present. Update all `Src:` fields to new BI-codes after deduplication.
8. **Token counting** Render draft markdown; if > 7 000 tokens → a) remove `Imp=m` Principles, list them under `#Tail:`; b) trim quotes/examples > 10 words. Re-count tokens; repeat until ≤ 7 000.
9. **Final assemble** Insert all sections exactly as in block «2 · Final output». Replace `{PROJECT}` with user-specified domain. Stamp `#MERGE completed` with today’s UTC date.
10. **Deliver** Output final markdown **without** this INTERNAL STEPS block.
###################################################################################### -->