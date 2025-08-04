# Dashboard Module

This folder contains the Streamlit application used for interactive portfolio monitoring and visualisation.

## Files

| File | Purpose |
|------|---------|
| `dashboard.py` | Main Streamlit app. Presents NAV charts, allocation pies, P&L tables, SEC snippets and back-test comparison. |
| `run_dashboard.sh` | Convenience launcher that calls Streamlit from the project’s `.venv`. Useful outside VS Code where auto-activation might fail. |

## Data Flow

1. **Portfolio CSV**  
   * If `data/portfolio.csv` exists → load it.  
   * Else prompt the user to upload an Interactive Brokers export.  
   * Additionally, if a recent export is found under `memory_bank/active_memory/portfolio/`, it is pre-selected.
2. **Parsing**  
   `parse_positions()` extracts asset class, symbol, quantity, market value and unrealised P&L.  
   Missing sector info is filled via `yfinance`.
3. **Visuals**  
   * Pie charts for allocation (asset class / sector).  
   * Bar chart for top N positions.  
   * NAV and performance curves built from raw report lines.  
   * Back-test comparison vs SPY & VNQ.  
   * Latest SEC Risk-Factors snippets.

## Customisation

Feel free to copy `dashboard.py` and tweak the layout, charts, or data sources to match your personal workflow. The goal of this app is to visualise key portfolio metrics that are hard to grasp through raw text in chat: NAV curves, allocation pies, option spreads, back-test equity lines, etc.

## Running

```bash
# Recommended: VS Code auto-activates .venv; otherwise activate manually
./tools/dashboard/run_dashboard.sh
# or
streamlit run tools/dashboard/dashboard.py
```

The dashboard listens by default on `localhost:8501`. Use the Streamlit `--server.address` flag to change the bind address if needed (remember the project’s privacy rule: keep it localhost).
