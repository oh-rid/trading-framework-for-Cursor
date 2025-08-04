#!/usr/bin/env python3
"""Fetch SEC Risk Factors (Item 1A) for a given ticker.

Usage:
    python tools/sec/fetch_sec.py TSLA

The script:
1. Loads the SEC_API_KEY environment variable (from .env) via python-dotenv;
2. Fetches the latest company 10-K or 10-Q via sec-api;
3. Extracts the "Item 1A – Risk Factors" section;
4. Saves the result as Markdown:
   data/sec_data/<TICKER>_<YYYY-MM-DD>_RiskFactors.md
"""
from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
import sys

from dotenv import load_dotenv
from sec_api import QueryApi, ExtractorApi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_latest_filing(ticker: str, api_key: str) -> dict | None:
    """Return metadata of the latest 10-K/10-Q filing for ticker."""
    query_api = QueryApi(api_key=api_key)

    query = {
        "query": {
            "query_string": {
                "query": f"ticker:{ticker.upper()} AND (formType:\"10-K\" OR formType:\"10-Q\")"
            }
        },
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}],
    }

    result = query_api.get_filings(query)
    filings = result.get("filings", []) if isinstance(result, dict) else []
    return filings[0] if filings else None


def extract_risk_factors(filing_url: str, api_key: str) -> str:
    """Return plain-text of Item 1A Risk Factors section."""
    extractor_api = ExtractorApi(api_key)
    return extractor_api.get_section(filing_url, "risk_factors", "text")


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------

def main() -> None:
    # Load .env from the project root even if cwd changed
    repo_root = Path(__file__).resolve().parents[2]  # ../../../ → repo root
    load_dotenv(dotenv_path=repo_root / ".env", override=True)
    api_key = os.getenv("SEC_API_KEY")
    if not api_key:
        print("ERROR: SEC_API_KEY not found in environment. Add it to .env", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Fetch SEC Risk Factors (Item 1A)")
    parser.add_argument("ticker", help="Stock ticker symbol, e.g. AAPL")
    args = parser.parse_args()

    ticker = args.ticker.upper()

    filing = get_latest_filing(ticker, api_key)
    if not filing:
        print(f"No 10-K/10-Q filings found for {ticker}.", file=sys.stderr)
        sys.exit(2)

    filing_url: str = filing.get("linkToFilingDetails") or filing.get("filingUrl")
    filed_at: str = filing.get("filedAt", "")[:10]  # 'YYYY-MM-DD'
    form_type: str = filing.get("formType", "10-K/10-Q")

    if not filing_url:
        print("Filing URL not found in API response.", file=sys.stderr)
        sys.exit(3)

    # Determine section ID depending on form type
    section_id = "risk_factors" if form_type.startswith("10-K") else "part2item1a"

    try:
        extractor_api = ExtractorApi(api_key)
        risk_text = extractor_api.get_section(filing_url, section_id, "text")
    except Exception as exc:
        print(f"Failed to extract risk factors ({section_id}): {exc}", file=sys.stderr)
        sys.exit(4)

    if not risk_text.strip():
        print("Risk Factors section empty or not found.", file=sys.stderr)
        sys.exit(5)

    save_dir = Path("data/sec_data")
    save_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{ticker}_{filed_at}_RiskFactors.md"
    file_path = save_dir / file_name

    header = f"# Item 1A – Risk Factors\n\n*{ticker} – {form_type} filed {filed_at}*\n\n"
    file_path.write_text(header + risk_text.strip() + "\n")

    print(f"✔ Saved → {file_path}")


if __name__ == "__main__":
    main()
