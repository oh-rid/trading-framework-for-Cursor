# SYSTEM  (Merge-Mindsets-MD mode)

INPUT — folder with *_mindset.md files (one per analyst).

OUTPUT FILE  `meta_investor_framework.md`
# Meta-Investor Framework  (ver. 2025-07-31)

## I. Layer Stack
### Liquidity
| Metric | Global Weight | UpdateFreq | Signal Map (who / threshold) |
|--------|--------------|------------|------------------------------|
| NetLiquidity | 0.22 | Weekly | Alden >+200 bn; Kelly >+180 bn; ... |

*(repeat for Macro, RegGeo, On-chain, Psychology)*

## II. Risk Kernel
- **Kelly Core:** yes  
- **θ-Sizing:** yes  
- **Cut-Fast (Druckenmiller):** yes  
- **Stop-Grid:** maxDD −35 %, posLimit 4 % NAV

## III. Bias Firewall (Top-5)
1. Confirmation  
2. Anchor  
3. Overconfidence  
4. Recency  
5. Survivorship

## IV. Analysts Weights
| Analyst | Weight | Dominant Bias |
|---------|--------|---------------|
| Lyn Alden | 0.17 | Anchor |
| Luke Gromen | 0.11 | Confirmation |
| … | … | … |

## V. Conflict-Panel Trigger
Fires if the weight-adjusted metric diverges > 15 p.p.

## VI. Missing Sources
- <file>, p. N  – CitationPending

REQUIREMENTS  
• Length ≤ 1 000 words.  
• Every metric must have Layer and Weight.  
• Σ Weights = 1 (show normalization formula).

CHAT OUTPUT  
▸ Link `[Download meta_investor_framework.md](sandbox:/mnt/data/meta_investor_framework.md)`  
▸ Executive summary ≤ 120 words.
