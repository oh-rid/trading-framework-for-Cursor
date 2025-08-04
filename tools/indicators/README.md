# Analyst Indicators — Data Collector

A Python utility that automatically gathers the key macro, liquidity and crypto indicators followed by leading analysts and traders.

## Data Sources

### TWS (Interactive Brokers) — free
- **UST 30Y Yield** — US 30-Year Treasury Bond future
- **UST 10Y Yield** — US 10-Year Treasury Note future  
- **DXY Index** — US Dollar Index  
- **VIX Index** — CBOE Volatility Index  
- **Gold Price** — Gold futures (GC) or GLD ETF  
- **BTC Price** — Bitcoin futures or IBKR crypto feed  
- **Funding Rate** — Crypto perpetual futures (via exchange API)

### FRED API (St. Louis Fed) — free
- **Global M2** — M2SL  
- **ISM PMI** — NAPM (Manufacturing PMI)  
- **Fed Balance Sheet** — WALCL  
- **Real 10Y Rate** — DGS10 – CPI  
- **Debt-to-GDP** — GFDEBTN / GDP

### Treasury.gov — free
- **TGA Balance** — Treasury General Account  
- **RRP Volume** — Reverse Repo operations

### CoinGecko API — free (rate-limited)
- **BTC Price**  
- **BTC Dominance**  
- **DeFi TVL** — basic version

### Custom Calculations
- **NetLiquidity** = Fed Assets − TGA − RRP  
- **BTC Stock-to-Flow** = BTC Supply / Annual Production  
- **VaR Portfolio** = calculated from current IBKR positions

---

## Installation

```bash
pip install -r requirements.txt
```

## API Keys

### FRED (required for Treasury data)
1. Register at <https://fred.stlouisfed.org/>  
2. Obtain an API key: <https://fred.stlouisfed.org/docs/api/api_key.html>  
3. Add to environment:
   ```bash
   export FRED_API_KEY="your_key_here"
   ```

### TWS (Interactive Brokers)
- Make sure TWS or IB Gateway is running and the API port is enabled.  
- Check the port in **Settings → API → Socket Port**.

### `.env` shortcut
You can also place keys in a `.env` file at project root:
```
FRED_API_KEY=...
BYBIT_API_KEY=...
BYBIT_API_SECRET=...
```

---

## Usage Examples

```bash
# Collect all indicators
python tools/indicators/collect_indicators.py

# Collect only TWS data
python tools/indicators/collect_indicators.py --source tws

# Collect only FRED data
python tools/indicators/collect_indicators.py --source fred

# Save output to CSV
python tools/indicators/collect_indicators.py --output indicators.csv

# Run unit test without TWS
python tools/indicators/test_indicators.py

# Collect only public data (no TWS / FRED)
python tools/indicators/collect_indicators.py --source treasury coingecko custom
```

---

## Output Schema
The script emits a timestamped JSON saved to `data/indicators/`:

```json
{
  "timestamp": "2025-08-01T17:03:06Z",
  "indicators": {
    "liquidity": {
      "net_liquidity": {"value": 6010.30, "source": "custom", "status": "ok"},
      "tga_balance":   {"value": 417.83,  "source": "treasury", "status": "ok"},
      "rrp_volume":    {"value": 214.45,  "source": "treasury", "status": "ok"}
    },
    "macro": {
      "ust_30y":          {"value": 4.89,     "source": "fred_fallback", "status": "ok"},
      "dxy":              {"value": 120.41,   "source": "fred_fallback", "status": "ok"},
      "fed_balance_sheet": {"value": 6642.58, "source": "fred",         "status": "ok"}
    },
    "crypto": {
      "btc_price":     {"value": 45000, "source": "tws",       "status": "ok"},
      "btc_dominance": {"value": 52.3,  "source": "coingecko", "status": "ok"}
    }
  }
}
```

`status` fields:  
- `ok` — data fetched successfully  
- `error` — fetch error  
- `pending` — data gathering in progress  
- `no_data` — not available

---

## Contributing / Extending
* Add new fetchers in `collect_indicators.py` and register them in the `SOURCE_MAP`.  
* Follow PEP-8 and add type annotations.  
* Provide unit tests (`tests/`) for non-trivial logic.

© 2025