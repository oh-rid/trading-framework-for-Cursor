### PROPERTY_DISTILLATE v1.0

#### Meta Layer
BigIdeas: BI01, BI02, BI03, BI04, BI05, BI06, BI07, BI08  
MetaPrinciples:
[M01] Diversification across property types and regions lowers idiosyncratic risk | Conf:0.72 | Imp:M | Src:BI01
[M02] Correlations spike during stress, reducing diversification | Conf:0.78 | Imp:C | Src:BI02
[M03] Dividend safety depends on payout vs. AFFO | Conf:0.80 | Imp:C | Src:BI03
[M04] Dry powder concentrates in mega-funds, raising deployment pressure | Conf:0.75 | Imp:M | Src:BI04
[M05] CPI indexation supports real cash flows | Conf:0.76 | Imp:M | Src:BI05
[M06] Value creation via leasing, capex and capital-structure optimisation | Conf:0.80 | Imp:C | Src:BI06
[M07] Asset purchases shift demand toward yield assets | Conf:0.82 | Imp:C | Src:BI07
[M08] Payment-to-income channel transmits rate shocks quickly | Conf:0.80 | Imp:C | Src:BI08
KeyFormulas: F01  
Glossary add: –

---

#### Principles
[P01] Track FFO growth | Works: stable demand | Fails: falling occupancy | Act: favour REITs with FFO CAGR > 5 % | Conf:0.65 | Imp:M | Tags:M=QE;C=EZ | Bias:B01 | Src:BI01  
[P02] Rotate sectors across cycle | Works: timing right | Fails: mistimed rotation | Act: rebalance quarterly | Conf:0.60 | Imp:m | Tags:S=UP | Bias:B02 | Src:BI01  
[P03] Monitor rolling correlations | Works: volatile regimes | Fails: stable periods | Act: update matrix monthly | Conf:0.70 | Imp:M | Tags:M=QE;C=EZ | Bias:B03 | Src:BI02  
[P04] Hold liquidity buffers | Works: contagion events | Fails: cash drag | Act: keep 5-10 % cash | Conf:0.65 | Imp:m | Tags:R=GR | Bias:B04 | Src:BI02  
[P05] Prioritise management alignment | Works: insider > 3 % | Fails: empire building | Act: review proxies annually | Conf:0.75 | Imp:M | Tags:C=EZ | Bias:B05 | Src:BI03  
[P06] Buy below NAV discount > 15 % | Works: undervaluation | Fails: hidden impairments | Act: use NAV screen | Conf:0.70 | Imp:M | Tags:I=DI | Bias:B06 | Src:BI03  
[P07] Monitor interest-coverage ratio > 3× | Works: prudent leverage | Fails: covenant breach | Act: avoid over-levered REITs | Conf:0.68 | Imp:M | Tags:M=QE | Bias:B07 | Src:BI03  
[P08] Lower IRR targets by +150 bps | Works: high-rate plateau | Fails: rapid easing | Act: adjust hurdle | Conf:0.70 | Imp:M | Tags:M=QT | Bias:B08 | Src:BI04  
[P09] Allocate to Oslo CBD offices | Works: limited supply | Fails: remote-work shift | Act: overweight core Oslo | Conf:0.68 | Imp:M | Tags:S=UP | Bias:B09 | Src:BI05  
[P10] Underwrite exit cap +50 bps | Works: conservative | Fails: unexpected compression | Act: stress-test | Conf:0.70 | Imp:M | Tags:C=EZ | Bias:B10 | Src:BI06  
[P11] Use moderate leverage 50-60 % LTV | Works: growth | Fails: downturn | Act: lock fixed debt | Conf:0.68 | Imp:M | Tags:M=QE | Bias:B11 | Src:BI06  
[P12] Analyse cap-rate beta to real yield | Works: QE | Fails: taper | Act: run regression | Conf:0.75 | Imp:M | Tags:M=QE | Bias:B12 | Src:BI07  
[P13] Stress-test affordability +300 bps | Works: prudent underwriting | Fails: teaser rates | Act: rate floors | Conf:0.78 | Imp:M | Tags:M=QT | Bias:B13 | Src:BI08  
[P14] Prefer amortising loans | Works: deleveraging | Fails: interest-only | Act: limit IO share | Conf:0.72 | Imp:M | Tags:C=EZ | Bias:B14 | Src:BI08

---

#### ConceptGraph
InterestRates → influence → CapRates  
GDPGrowth → drives → RentalDemand  
MarketStress → increases → Correlation  
Liquidity → mitigates → Drawdown  
FFO → supports → Dividends  
Leverage → affects → Risk  
ManagementAlignment → drives → CapitalAllocation  
HigherRates → suppress → Valuations  
DryPowder → increases → Competition  
CPI → escalates → Rent  
OilPrice → impacts → LeasingDemand  
ActiveManagement → increases → NOI  
Leverage → magnifies → Returns  
Capex → enhances → Value  
QE → reduces → Yields  
LowerYields → compress → CapRates  
RateShock → raises → DSCR  
HighLTV → increases → DefaultProbability

---

#### KeyFormulas
[F01] DSCR = NetIncome / DebtService | Expl.: ability to cover payments | Conf:0.70 | Imp:M | Src:BI08

---

#### Glossary
Glossary add: –

---

#### Bias Glossary
[B01] Recency = Overweighting recent trends  
[B02] TimingIllusion = Confidence in short-term cycles  
[B03] Herding = Crowd-following under stress  
[B04] CashDrag = Fear of underperformance holding cash  
[B05] Agency = Managers act in own interest  
[B06] ValueTrap = Cheap for a reason  
[B07] LeverageOptimism = Underestimating debt risk  
[B08] ReturnAnchoring = Using outdated IRR benchmarks  
[B09] HomeBias = Preference for familiar cities  
[B10] OptimismBias = Underestimating cap-rate expansion risk  
[B11] LeverageComfort = Assuming refinancing ease  
[B12] PolicyPermanence = Assuming QE lasts indefinitely  
[B13] Optimism = Underestimating rate increases  
[B14] PaymentShock = Focusing on initial payment only

---

#### Tag Legend
| Cat | Codes | Meaning |
|-----|-------|----------|
| **M** | QE QT HR | Monetary regimes |
| **C** | EZ TI | Credit standards |
| **I** | DI SI | Inflation regimes |
| **S** | UP OS | Supply balance |
| **R** | GR TX | Regulation / Tax shocks |

`Tags:` — where the rule applies. `Fails:` — tags for which the rule is disabled.

*Imp (Impact):*  
• **C** Critical — breach = project/portfolio collapse  
• **M** Major — ±2 p.p. ROI or volatility > 30 %  
• **m** Minor — local effect < 2 p.p.

*Conf (Confidence):*  
0.90–1.00 = meta-analysis / ≥ 3 independent datasets, p < 0.01  
0.70–0.89 = peer-reviewed + ≥ 10 years of data  
0.40–0.69 = working paper, limited dataset  
0.10–0.39 = author's hypothesis / case study

---

#### SourceMap
BI01 = «2025 Global REIT Brochure, industry brochure»  
BI02 = «An Empirical Study on the Interconnections between REITs and Financial Markets, research paper»  
BI03 = «The Intelligent REIT Investor, book»  
BI04 = «McKinsey Global Private Markets Review 2024, report»  
BI05 = «Norwegian Commercial Real Estate Thesis, academic thesis»  
BI06 = «Private Real Estate Markets and Investment, textbook»  
BI07 = «QE to Real Estate, working paper»  
BI08 = «House Prices, Debt Burdens and Mortgage Rate Shocks, working paper»

#MERGE completed 2025-07-29  
#META BigIdeas: BI01, BI02, BI03, BI04, BI05, BI06, BI07, BI08 