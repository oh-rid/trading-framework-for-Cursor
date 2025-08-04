#!/usr/bin/env python3
"""tools/backtest/backtest.py

Простейший портфельный бэктестер.

Пример:
    python tools/backtest/backtest.py portfolio.csv 2018-01-01 2025-07-15 monthly

`portfolio.csv` ожидает столбцы:
Symbol,Quantity
AAPL,50
MSFT,30
...
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------


def _usage() -> None:  # noqa: D401
    print("usage: backtest.py <portfolio.csv> <start> <end> <freq>")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:  # noqa: D401
    if len(sys.argv) != 5:
        _usage()

    f_name, start, end, freq = sys.argv[1:]
    try:
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
    except ValueError:
        _usage()

    freq_map = {"monthly": "M", "quarterly": "Q", "yearly": "A"}
    if freq.lower() not in freq_map:
        sys.exit("freq must be one of: monthly, quarterly, yearly")

    # --- load portfolio ---
    df_port = pd.read_csv(f_name)[["Symbol", "Quantity"]]
    df_port["Quantity"] = pd.to_numeric(df_port["Quantity"], errors="coerce")
    df_port = df_port.dropna()
    if df_port.empty:
        sys.exit("portfolio.csv is empty or invalid")

    weights = df_port.set_index("Symbol")["Quantity"]
    weights = weights / weights.sum()

    # --- download prices (auto-adjusted) ---
    tickers = " ".join(weights.index)
    raw = yf.download(tickers, start=start_dt, end=end_dt, auto_adjust=True, progress=False)

    # yfinance для нескольких тикеров возвращает MultiIndex, где уровень 1 — 'Close', 'Open' и т.д.
    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw.xs("Close", level=0, axis=1)
    else:
        prices = raw  # одиночный тикер

    prices = prices.dropna(how="all")

    # align weights columns
    missing = [t for t in weights.index if t not in prices.columns]
    if missing:
        print(f"Warning: no price data for {missing}, they will be skipped")
        weights = weights.drop(missing)
    prices = prices[weights.index]

    # --- rebalance ---
    rebal_dates = pd.date_range(start_dt, end_dt, freq=freq_map[freq.lower()]).union([start_dt])
    rebal_dates = rebal_dates[rebal_dates.isin(prices.index)]

    portfolio = pd.Series(index=prices.index, dtype=float)
    last_rebal = rebal_dates[0]
    portfolio[last_rebal] = 1.0  # начальная стоимость 1

    for i in range(1, len(rebal_dates)):
        d_prev, d_cur = rebal_dates[i - 1], rebal_dates[i]
        # доходность между ребалансами
        ret = (prices.loc[d_prev:d_cur] / prices.loc[d_prev]).dot(weights)
        portfolio.loc[d_prev:d_cur] = portfolio.loc[d_prev] * ret
        last_rebal = d_cur

    # хвост до конца периода
    if last_rebal < prices.index.max():
        tail_ret = (prices.loc[last_rebal:] / prices.loc[last_rebal]).dot(weights)
        portfolio.loc[last_rebal:] = portfolio.loc[last_rebal] * tail_ret

    # --- save results ---
    out_dir = Path("data/backtests")
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = Path(f_name).stem + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M")

    plt.figure(figsize=(8, 4))
    portfolio.plot(title="Backtest cumulative return")
    plt.xlabel("Date")
    plt.ylabel("Growth of 1$")
    png_path = out_dir / f"{tag}.png"
    plt.savefig(png_path, bbox_inches="tight")
    plt.close()

    # prepare header metadata
    first_prices = prices.loc[prices.index[0]].to_dict()
    last_prices = prices.loc[prices.index[-1]].to_dict()

    header_lines: list[str] = []
    header_lines.append(f"# REBALANCE_FREQ,{freq.lower()}")
    header_lines.append(
        "# INITIAL_PRICES," + ",".join(f"{t}:{p:.4f}" for t, p in first_prices.items())
    )
    header_lines.append(
        "# FINAL_PRICES," + ",".join(f"{t}:{p:.4f}" for t, p in last_prices.items())
    )

    # --- risk metrics ---
    daily_ret = portfolio.dropna().pct_change().dropna()
    if not daily_ret.empty:
        mean_ret = daily_ret.mean()
        vol = daily_ret.std()
        sharpe = (mean_ret / vol) * (252 ** 0.5) if vol else 0.0

        downside = daily_ret[daily_ret < 0]
        dd_std = downside.std()
        sortino = (mean_ret / dd_std) * (252 ** 0.5) if dd_std else 0.0

        header_lines.append(f"# SHARPE,{sharpe:.4f}")
        header_lines.append(f"# SORTINO,{sortino:.4f}")

    csv_path = out_dir / f"{tag}.csv"
    with open(csv_path, "w", newline="") as fh:
        for ln in header_lines:
            fh.write(ln + "\n")
        portfolio.to_csv(fh, header=["Portfolio"], index_label="Date")

    print("✔ saved →", png_path)


if __name__ == "__main__":
    main() 