"""CLI wrapper for the Bybit connector.

Usage:
    python tools/bybit/bybitctl.py --coin BTC
"""
from __future__ import annotations

import argparse
import json

from tools.bybit.bybit_core import BybitConnector


def _cli() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Query Bybit wallet balance via CLI.")
    parser.add_argument("--coin", help="Coin code (e.g. BTC, USDT). If omitted – fetch all.")
    parser.add_argument("--testnet", action="store_true", help="Use Bybit testnet endpoint.")
    args = parser.parse_args()

    connector = BybitConnector(testnet=args.testnet)
    balance = connector.get_balance(coin=args.coin)
    print(json.dumps(balance, ensure_ascii=False, indent=2))


if __name__ == "__main__":  # pragma: no cover
    _cli()