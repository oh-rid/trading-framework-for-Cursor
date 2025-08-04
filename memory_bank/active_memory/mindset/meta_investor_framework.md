# Meta-Investor Framework (ver. 2025-07-31)

## I. Layer Stack

### Liquidity

| Metric | Global Weight | Update Freq | Signal Map (who / threshold) |
|--------|--------------|------------|------------------------------|
| NetLiquidity | 0.18 | Weekly | KK > +200 bn; AP > +200 bn; LA > +180 bn |
| TGA Balance | 0.12 | Daily | AH declining; LA declining; LG < $200 bn |
| RRP Volume  | 0.10 | Daily | AH falling; LG falling; KK < $100 bn |
| Global M2   | 0.08 | Monthly | AH rising; DM rising; AK rising |

### Macro

| Metric | Global Weight | Update Freq | Signal Map (who / threshold) |
|--------|--------------|------------|------------------------------|
| UST 30Y Yield | 0.08 | Daily | SD < 4 %; AP < 3.5 % |
| DXY Index | 0.06 | Daily | SD falling; LG < 50 % reserves |
| Fed Balance Sheet | 0.06 | Weekly | SD expanding; KK expanding |
| Debt-to-GDP | 0.05 | Quarterly | LA < 100 %; LG > 120 % |

### Risk

| Metric | Global Weight | Update Freq | Signal Map (who / threshold) |
|--------|--------------|------------|------------------------------|
| VaR Portfolio | 0.08 | Daily | AK < 5 %; JA < 1 %; AP < 1 % |
| VIX Index | 0.04 | Daily | KK < 20; SD < 25 |
| Funding Rate | 0.03 | 8 h | AK negative; JA negative |

### Crypto

| Metric | Global Weight | Update Freq | Signal Map (who / threshold) |
|--------|--------------|------------|------------------------------|
| BTC Price | 0.06 | Daily | AH > $90k; DM > $100k |
| BTC Dominance | 0.03 | Daily | DM > 50 %; LA > 45 % |
| Active Addresses | 0.02 | Daily | DM rising |

**Σ Weights = 1.00** (normalization: 18 + 12 + 10 + 8 + 8 + 6 + 6 + 5 + 8 + 4 + 3 + 6 + 3 + 2 = 100 %)

## II. Risk Kernel

- **Kelly Core:** ✅ Multivariate analysis with factor confluence  
- **θ-Sizing (AP):** ✅ Position-sizing algorithm based on probability  
- **Cut-Fast (SD):** ✅ Quick exit from losing ideas without price anchoring  
- **Stop-Grid:** maxDD −35 % (DM), posLimit 4 % NAV (AK)

## III. Bias Firewall (Top-5)

1. **Confirmation** – counter-narrative check (JA), premortem analysis (KK)  
2. **Anchor** – avoiding entry-price anchoring (SD)  
3. **Overconfidence** – pause-before-click (AP), public invalidation (AK)  
4. **Recency** – focus on long-term trends (LG, LA)  
5. **Survivorship** – handled in VaR models (AP)

## IV. Analysts Weights

| Analyst | Weight | Dominant Bias | Key Contribution |
|---------|--------|---------------|------------------|
| LA | 0.15 | Anchor | Fiscal dominance, TGA/RRP |
| LG | 0.12 | Confirmation | Triffin's Dilemma, dollar system |
| SD | 0.14 | Overconfidence | Liquidity, quick decisions |
| KK | 0.13 | Confirmation | Net Liquidity, reflexivity |
| AH | 0.11 | Recency | Left Curve, liquidity driver |
| AK | 0.10 | Loss aversion | Contrarian approach, VaR control |
| DM | 0.08 | Optimism | Escape velocity, S-curves |
| JA | 0.09 | Ownership | PvP market, asymmetric bets |
| AP | 0.08 | Carry trap | LGI matrix, θ-sizing |

**Σ Weights = 1.00** (normalization: 15 + 12 + 14 + 13 + 11 + 10 + 8 + 9 + 8 = 100 %)

## V. Conflict-Panel Trigger

Activated when the metric-weight corrector diverges by more than 15 p.p.

**Conflict examples:**  
- **UST 30Y:** SD < 4 % vs AP < 3.5 % (12.5 % divergence)  
- **BTC Price:** AH > $90k vs DM > $100k (10 % divergence)  
- **VaR:** AK < 5 % vs JA < 1 % (80 % divergence) → **TRIGGER**

## VI. Missing Sources

- **ISM PMI:** KK uses series, but it is unavailable in FRED  
- **MOVE Index:** KK uses Bloomberg feed, unavailable in TWS  
- **DeFi TVL:** DM relies on DeFiPulse; API unstable  
- **CVD/MEV:** JA leverages proprietary internal data  

## Executive Summary (120 words)

Meta-Investor Framework fuses the insights of nine leading analysts into a unified decision system built on fourteen metrics grouped across liquidity, macro, risk and crypto layers. Liquidity (48 %) and macro (25 %) dominate the weight allocation, reflecting their outsized impact on returns. The Risk Kernel combines LA’s multivariate Kelly Core, AP’s probability-based θ-sizing, SD’s Cut-Fast discipline and DM’s Stop-Grid drawdown guard. A five-layer Bias Firewall counters confirmation, anchoring and overconfidence. Analyst weights favour LA (15 %) and SD (14 %), ensuring balanced macro and tactical perspectives. The conflict panel flags material signal divergence (> 15 p.p.) for rapid review. Designed for automation, the framework integrates seamlessly with `collect_indicators.py` to keep metrics fresh and actionable.
