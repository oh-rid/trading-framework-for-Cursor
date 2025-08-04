### 📑 UNIVERSAL DISTILLATION PROMPT (v4.4 · 2025‑07‑29)

##### LLM‑USAGE  (≤ 40 words)
- Treat rules as priors, not dogma.  
- You may override if new evidence ≥ Conf of prior.  
- Cite principle ID when disagreeing.  
- Bias‑check before applying any rule.  
- Keep output ≤ 1500 tokens.

<!--
########################  INTERNAL GUIDANCE – NOT FOR OUTPUT  ########################

FIELD RULES
• Conf (confidence):
  - 0.90–1.00  meta‑analysis, ≥3 datasets, p < 0.01
  - 0.70–0.89  peer‑review + ≥10 y data
  - 0.40–0.69  working paper, limited data
  - 0.10–0.39  author opinion / case study

• Imp (impact):
  - C Critical — bankruptcy / portfolio crash
  - M Major    — ±200 bps ROI or vol > 30 %
  - m Minor     — local effect < 200 bps

• Flex:             Core = follow strictly; Advisory = may ignore with reason.

• Tags / Fails:
  1. Describe macro‑context where rule *works* (`Tags:`) and *breaks* (`Fails:`).
  2. Use only codes from Tag Legend, format `Cat=Code` separated by `;`.
  3. Min 1 code in either Tags or Fails, OR write `Tags: ALWAYS`.
  4. Max total 6 codes (e.g., 3 Tags + 3 Fails) to avoid over‑specification.

ALGORITHM
1. Read source, write BigIdea ≤ 25 words.
2. Extract meta‑principles (if any) → MetaPrinciples.
3. For each actionable rule:
   a. Fill Works / Fails / Act concisely.
   b. Score Conf & Imp; set Flex; add Tags / Fails / Bias / Src.
4. Build ConceptGraph (≤ 5 directed triples).
5. Add KeyFormulas if present.
6. Append new Glossary T‑codes & Bias B‑codes (see criteria below).
7. Check token budget; if > 1500, drop Imp=m lines & list them under #Tail.
8. Ensure output structure matches section 3 exactly – no extra text.

TERMINOLOGY / GLOSSARY
Include a term only if it meets *any* of:
  • appears < 3× in standard industry texts;
  • coined by the author (e.g., PropTech‑Alpha™);
  • re‑defines a classic term in a novel way;
  • used ≥ 2× in Principles or Formulas and critical for comprehension.

######################################################################################
-->

##### Meta Layer
BigIdea **[BI1]** — ≤ 25 words  
MetaPrinciples:                <!-- optional; include only if present -->
[M1s] Statement | Conf:0.82 | Imp:C | Src:BI1
KeyFormulas: F1,F2  or "–"  
Glossary add: T‑codes or "–"

##### Principles  (Imp = C/M mandatory; Imp = m allowed while total ≤ 1500 tokens)
[P1] Title | Works: … | Fails: … | Act: … | Conf:0.88 | Imp:C | **Flex:Core**  
| Tags: M=QE;C=EZ           # positive contexts  
| Fails: M=QT               # break contexts  
| Bias:B1 | Src:BI1  
[… additional P‑lines …]  
#Tail: P12 P15 …   <!-- list ONLY Imp=m rules removed due to token limit; omit if none -->

##### ConceptGraph  (≤ 5 triples “A → relation → B”)
A → relation → B

##### KeyFormulas  (if any)
[F1] Formula = … | Expl.: … | Conf:0.70 | Imp:M | Src:BI1

##### Glossary  (new T‑codes)  Bias Glossary — next section
[T1] Term = ≤ 12 words definition | Src:BI1  
…  
If no new terms satisfy criteria → write `Glossary add: –`.

##### Bias Glossary  (new B‑codes)
[B1] BiasName = short explanation  
…

##### Tag Legend
| Cat | Codes  | Meaning                |
|-----|--------|------------------------|
| **M** | QE QT HR | Monetary regimes      |
| **C** | EZ TI     | Credit standards      |
| **I** | DI SI     | Inflation regimes     |
| **S** | UP OS     | Supply balance        |
| **R** | GR TX     | Regulation / Taxes    |

`Tags:` — contexts where rule is valid. `Fails:` — contexts where effect vanishes or reverses.

*Imp (Impact):* C > M > m  *Conf (Confidence):* see table above.

##### Conflicts / Alternatives  (≤ 20 words)
- …

##### SourceMap
BI1 = «Smith J., “Real‑Estate Cycles Explained”, 2024, book»  
BI2 = …  
…

#META BigIdea: BI1
