import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import re
import subprocess, sys

"""
Streamlit dashboard for Interactive Brokers CSV exports.

Personal identifiers and example file names were stripped; you can adjust
`DEFAULT_CSV` and `SEC_PATH` to point at your own data.
"""

# ------------------------------------------------------------------
# Config – change these to your own files / folders
# ------------------------------------------------------------------

PORTFOLIO_DIR = Path("memory_bank/active_memory/portfolio")
# pick the newest CSV from the memory bank as the default source
def _latest_csv(directory: Path) -> Path | None:
    csvs = list(directory.glob("*.csv"))
    return max(csvs, key=lambda p: p.stat().st_mtime) if csvs else None

DEFAULT_CSV = _latest_csv(PORTFOLIO_DIR)  # may be None on first run
PORTFOLIO_CSV = PORTFOLIO_DIR / "positions_latest.csv"
SEC_PATH = Path("data/sec_data")  # folder with *_RiskFactors.md files

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------


def load_csv(content: bytes) -> list[str]:
    """Decode uploaded CSV bytes to list of raw lines."""
    return content.decode("utf-8", errors="ignore").splitlines()


def parse_positions(raw_lines: list[str]) -> pd.DataFrame:
    """Extract open positions block from IB Portfolio Analyst export."""
    records = []
    for line in raw_lines:
        parts = line.split(",")
        if len(parts) < 14:
            continue
        if parts[0] == "Open Position Summary" and parts[1] == "Data":
            if parts[3].strip().lower() == "total":
                continue
            asset_class = parts[3].strip()
            currency = parts[4].strip()
            symbol = parts[5].strip()
            sector = parts[7].strip() or None
            qty = float(parts[8] or 0)
            val = float(parts[10] or 0)
            cost = float(parts[11] or 0)
            pl = float(parts[12] or 0)
            fx = float(parts[13] or 1)
            if currency == "USD":
                value_usd, pl_usd = val, pl
                value_eur, pl_eur = val * fx, pl * fx
                cost_usd, cost_eur = cost, cost * fx
            else:  # assume base EUR
                value_eur, pl_eur = val, pl
                value_usd, pl_usd = val / fx, pl / fx if fx else (val, pl)
                cost_eur, cost_usd = cost, cost / fx if fx else cost
            records.append(
                {
                    "asset_class": asset_class,
                    "symbol": symbol,
                    "sector": sector,
                    "quantity": qty,
                    "value_usd": value_usd,
                    "value_eur": value_eur,
                    "pl_usd": pl_usd,
                    "pl_eur": pl_eur,
                    "pl_pct_usd": pl_usd / cost_usd * 100 if cost_usd else 0,
                    "pl_pct_eur": pl_eur / cost_eur * 100 if cost_eur else 0,
                }
            )
    return pd.DataFrame(records)


@st.cache_data(show_spinner=False)
def get_sector(symbol: str) -> str:
    try:
        return yf.Ticker(symbol).info.get("sector", "Unknown")
    except Exception:
        return "Unknown"


def ensure_sectors(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["sector"].isna() | (df["sector"] == "")
    if mask.any():
        df.loc[mask, "sector"] = df.loc[mask, "symbol"].apply(get_sector)
    return df

# ------------------------------------------------------------------
# Simple visuals – pie & bar helpers
# ------------------------------------------------------------------

def pie_chart(series: pd.Series, title: str):
    positive = series[series > 0]
    if positive.empty:
        st.info(f"No positive values for {title} pie chart.")
        return
    fig, ax = plt.subplots(figsize=(6, 6))
    labels = None if len(positive) > 8 else positive.index
    wedges, *_ = ax.pie(positive, labels=labels, autopct="%1.1f%%" if labels else None, startangle=140)
    ax.axis("equal")
    ax.set_title(title)
    if labels is None:
        ax.legend(wedges, positive.index, loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig)


def positions_bar(df: pd.DataFrame, currency: str):
    val_col = f"value_{currency.lower()}"
    data = df.sort_values(val_col, ascending=False).head(20)[["symbol", val_col]].set_index("symbol")
    fig, ax = plt.subplots(figsize=(8, 6))
    data[val_col].plot(kind="barh", ax=ax, color="#4da6ff")
    ax.invert_yaxis()
    ax.set_xlabel(f"Market Value ({currency})")
    st.pyplot(fig)

# ------------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Portfolio Viewer", layout="wide")
    st.title("📊 Portfolio Viewer – IB CSV")

    if PORTFOLIO_CSV.exists():
        df = pd.read_csv(PORTFOLIO_CSV)
        raw_lines = load_csv(DEFAULT_CSV.read_bytes()) if DEFAULT_CSV.exists() else []
    else:
        uploaded = st.file_uploader("Upload IB CSV export", type="csv")
        raw_lines = load_csv(uploaded.read()) if uploaded else load_csv(DEFAULT_CSV.read_bytes()) if DEFAULT_CSV.exists() else []
        df = ensure_sectors(parse_positions(raw_lines))
        if st.checkbox("Save parsed positions to data/portfolio/positions_latest.csv"):
            PORTFOLIO_CSV.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(PORTFOLIO_CSV, index=False)
            st.success("Positions saved for future sessions.")

    # Currency picker
    cur = st.sidebar.selectbox("Display currency", [col.split("_")[1].upper() for col in df.columns if col.startswith("value_")])

    st.subheader("Allocation by Asset Class")
    pie_chart(df.groupby("asset_class")[f"value_{cur.lower()}"] .sum(), "By Asset Class")

    st.subheader("Top positions")
    positions_bar(df, cur)

    st.subheader("Positions table")
    cols = ["asset_class", "symbol", "quantity", f"value_{cur.lower()}", f"pl_{cur.lower()}", f"pl_pct_{cur.lower()}"]
    st.dataframe(df[cols])

if __name__ == "__main__":
    main()
