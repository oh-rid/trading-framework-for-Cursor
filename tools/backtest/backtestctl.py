#!/usr/bin/env python3
"""tools/backtest/backtestctl.py

Thin wrapper so the chat agent can run backtests.
Example:
    ./tools/backtest/backtestctl.py portfolio.csv 2018-01-01 2025-07-15 monthly

After execution prints the path to the generated .png so Cursor turns it into a clickable link.
"""
from __future__ import annotations
import subprocess, sys, pathlib, tempfile, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = pathlib.Path(__file__).with_name("backtest.py")
OUT_DIR = ROOT / "data" / "backtests"


def main() -> None:  # noqa: D401
    if len(sys.argv) != 5:
        sys.exit(textwrap.dedent(
            """
            usage:
              backtestctl.py <portfolio.csv> <start> <end> <freq>
              backtestctl.py <tickers_inline> <start> <end> <freq>

            <tickers_inline> format: "AAPL:50,MSFT:30" (Quantity optional, defaults to 1)
            """
        ).strip())

    csv_or_inline, start, end, freq = sys.argv[1:]

    # If the file doesn't exist, treat the argument as an inline ticker list
    csv_path = pathlib.Path(csv_or_inline)
    if not csv_path.exists():
        try:
            pairs = [p.strip() for p in csv_or_inline.split(",") if p.strip()]
            rows = []
            for pair in pairs:
                if ":" in pair:
                    sym, qty = pair.split(":", 1)
                    qty = float(qty)
                else:
                    sym, qty = pair, 1.0
                rows.append((sym.upper(), qty))
            if not rows:
                raise ValueError
        except Exception:
            sys.exit("Invalid inline tickers format. Use like 'AAPL:50,MSFT:30'")

        tmp = tempfile.NamedTemporaryFile("w", delete=False, suffix="_inline_port.csv", dir=pathlib.Path.cwd())
        csv_path = pathlib.Path(tmp.name)
        tmp.write("Symbol,Quantity\n")
        for sym, qty in rows:
            tmp.write(f"{sym},{qty}\n")
        tmp.flush()
        tmp.close()

    cmd = [sys.executable, str(SCRIPT), str(csv_path), start, end, freq]
    subprocess.run(cmd, check=True)

    # find the newest .png output
    try:
        latest = max(OUT_DIR.glob("*.png"))
        print(latest.relative_to(pathlib.Path.cwd()))
    except ValueError:
        sys.exit("No backtest output found")


if __name__ == "__main__":
    main() 