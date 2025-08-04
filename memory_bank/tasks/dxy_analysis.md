# DXY Indicator Analysis – Task List

## Problem
The experts’ mindset refers to a metric "DXY Index, weight 0.06" without clarifying which one—there are two candidates:
1. **ICE DXY** (the futures-based Dollar Index on NYBOT)
2. **FRED DTWEXBGS** (Broad Dollar Index published by the Fed)

## Tasks

### ✅ 1. Add both indicators to the system
- [x] Add `dxy_fred` (DTWEXBGS) to the FRED indicator set
- [x] Rename existing `dxy` to `dxy_ice` in the TWS indicator list
- [x] Test data collection for both

### 🔄 2. Scan key books – which DXY do the authors mean?

Books to review:
- [ ] Dynamic Hedging (Taleb)
- [ ] Interest Rate Markets (Jha)
- [ ] Economic Indicators (Steindel)
- [ ] McMillan on Options
- [ ] Sixth Street Investment Principles

Search questions:
1. **Mentions of DXY** – how exactly do authors reference the dollar index?
2. **Usage context** – hedging, macro analysis, trading?
3. **Data source** – FRED, Bloomberg, Reuters?
4. **Timeframe** – when was the book written (pre/post DTWEXBGS release)?

### 🔄 3. Compare indicator characteristics

#### ICE DXY (ticker: DXY)
- **Source:** ICE Futures
- **Type:** Futures contract
- **Basket:** 6 currencies (EUR, JPY, GBP, CAD, SEK, CHF)
- **Base year:** 1973 = 100
- **Update frequency:** Real-time

#### FRED DTWEXBGS (Broad Dollar Index)
- **Source:** Federal Reserve
- **Type:** Index
- **Basket:** 26 currencies (broader)
- **Base year:** 2006 = 100
- **Update frequency:** Daily

### 🔄 4. Determine the primary indicator

Criteria:
1. **Historical accuracy** – which better reflects macro trends?
2. **Data availability** – which is easier to fetch?
3. **Literature usage** – which is cited more often?
4. **Correlation with other indicators** – which integrates better in the model?

### 🔄 5. Update mindset dataset

After analysis:
- [ ] Decide on the correct DXY reference for the mindset
- [ ] Update weight and description
- [ ] Add the alternative index if needed

## Current Data Snapshot

### FRED DXY (DTWEXBGS): 120.4082
- Source: Federal Reserve
- Date: latest available
- Status: ✅ Working

### ICE DXY (DXY)
- Source: ICE Futures via TWS
- Status: ⏳ Requires TWS connection

## Next Steps
1. **Run book analysis** – use the prompt to search for DXY mentions
2. **Collect historical series** – compare indicator behavior
3. **Decide primary indicator** – based on analysis
4. **Update the system** – ensure the chosen DXY is in the mindset dataset
