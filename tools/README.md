# Tooling Overview

This directory groups all Python utilities and CLI entry-points that support data collection, research automation, back-testing, and brokerage connectivity. Each sub-folder is **self-contained**; use the slim CLI wrappers (`*_ctl.py`) for day-to-day interaction rather than importing modules manually.

> All tools assume a **Python 3.11** environment with the packages listed in `requirements.txt`.
> In VS Code / Cursor the interpreter **should be auto-picked** and each new terminal auto-activates the environment via `.vscode/settings.json`.
> If, for some reason, the auto-activation does not kick in, activate manually:
> `source .venv/bin/activate`.

## Contents

| Folder | Purpose | Main Entry-Point | Typical Output |
|--------|---------|------------------|----------------|
| `backtest/` | Run strategy simulations over historical price data. | `backtestctl.py` | `data/backtests/` CSV & PNG plots |
| `bybit/` | Pull positions / trades from the Bybit crypto exchange. | `bybitctl.py`, `bybit_core.py` | JSON / CSV snapshots |
| `chrome/` | Automation helpers for Google Chrome & IBKR WebTrader (profile switch, login pop-ups). | `chromectl.py` | none (side-effect scripts) |
| `IBRK/` | Connect to Interactive Brokers TWS / IB Gateway; export portfolio, place orders. | `ibrkctl.py`, `export_portfolio.py` | `data/portfolio/` CSV snapshots |
| `indicators/` | Collect macro, liquidity and crypto indicators from FRED, custom APIs. | `collect_indicators.py` | `data/indicators/` JSON files |
| `dashboard/` | Streamlit portfolio dashboard | `dashboard.py` | Local web UI (localhost:8501) |
| `research/` | Multi-agent research orchestrator (deep dives, PDF summarisation). | `researchctl.py`, `deep_research.py` | `data/deep_research/` Markdown reports |
| `sec/` | Download and parse SEC filings (10-K/10-Q). | `secctl.py`, `fetch_sec.py` | `data/sec_data/` Markdown summaries |

---


## Coding Conventions

1. **CLI first**: every tool exposes a `__main__` or dedicated `*_ctl.py` for non-interactive use.  
2. **Pure functions**: core logic sits in helper modules; CLI layers only parse args and handle I/O.  
3. **Typed**: annotate new code with `typing`.  
4. **Logs**: emit structured logs (`logging`, JSON friendly) at `INFO` level.  
5. **No secrets**: read API keys from environment variables (see `.env.example`).

---

## Folder Details

### backtest/
* `backtest.py` – generic vectorised engine (Pandas, NumPy).  
* `backtestctl.py` – CLI wrapper (`run`, `plot`, `benchmark`).

### bybit/
* `bybitctl.py` – fetch account positions, funding rates, trades.
* Requires `BYBIT_API_KEY` and `BYBIT_API_SECRET` set in `.env` (or exported to the shell).

### chrome/
* `chromectl.py` – AppleScript-based profile launcher (Mac only; sometimes the open-source **Browser MCP** utility works better—consider it as an alternative).  
* `profiles/*.yaml` – reusable Chrome profile templates.

### IBRK/
* `export_portfolio.py` – dumps position CSV via IB API.  
* `ibrkctl.py` – experimental higher-level CLI (orders, market data).
* Requires Interactive Brokers **TWS or IB Gateway running and API enabled** (double-check the API port set in your TWS/Gateway preferences).

### indicators/
* `collect_indicators.py` – pulls FRED, treasury APIs, crypto endpoints and calculates composite metrics.
* Requires `FRED_API_KEY` in `.env` for higher rate limits (falls back to public endpoints if absent).

### dashboard/
* `dashboard.py` – Streamlit app for portfolio visualisation.  
* `run_dashboard.sh` – helper launcher (uses local `.venv`).

### research/
* `deep_research.py` – single-topic deep-dive generator (LLM + retrieval).  
* `researchctl.py` – orchestrates multi-agent runs; integrates with prompts in `prompts/`.

### sec/
* `fetch_sec.py` – low-level EDGAR scraper.  
* `secctl.py` – CLI for common tasks (`fetch`, `diff`, `summarise`).

---

## Contribution Guidelines

1. Follow PEP-8 and black formatting.  
2. Include a short docstring at the top of every new script.  
3. Add unit tests in a sibling `tests/` directory if logic is non-trivial.  
4. Update this README when introducing a new tool or breaking change.

Happy hacking! :rocket:
