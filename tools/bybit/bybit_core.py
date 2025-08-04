"""Core Bybit connector logic extracted from bybitctl.py.

Provides a thin wrapper around the official Bybit REST SDK (`pybit`).
Import `BybitConnector` from this module in your Python code or let
`bybitctl.py` handle CLI interaction.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

try:
    # The official Bybit SDK (unified_trading) is part of the `pybit` package
    from pybit.unified_trading import HTTP
except ImportError as e:  # pragma: no cover
    raise ImportError("pybit package is required. Install with `pip install pybit`.") from e

# Load .env variables (two levels up from this file)
load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)


class BybitConnector:
    """Lightweight Bybit REST connector.

    API key and secret are read from environment variables:
    - BYBIT_API_KEY
    - BYBIT_API_SECRET
    """

    def __init__(self, testnet: bool = False) -> None:
        api_key = os.getenv("BYBIT_API_KEY")
        api_secret = os.getenv("BYBIT_API_SECRET")
        if not api_key or not api_secret:
            raise EnvironmentError(
                "Environment variables BYBIT_API_KEY and BYBIT_API_SECRET must be set.")

        self._session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------
    def get_balance(self, account_type: str = "UNIFIED", coin: str | None = None) -> Dict[str, Any]:
        """Return current wallet balance."""
        response = self._session.get_wallet_balance(accountType=account_type, coin=coin)
        if response.get("retCode") != 0:
            raise RuntimeError(f"Bybit API error: {response}")
        return response["result"]
