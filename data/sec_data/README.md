# SEC Data Exports

This folder collects filings and processed artefacts fetched from the U.S. SEC website via the utilities in `tools/sec/` (e.g., `secctl.py`, `fetch_sec.py`).

Typical files:

- Risk factor sections extracted from 10-K / 10-Q filings (`<ticker>_<YYYY-MM-DD>_RiskFactors.md`).
- JSON or CSV snapshots of specific disclosure items.

To add new data, instruct ChatGPT in agentic mode to run the SEC tool which scrapes/ downloads the desired filing and saves the parsed output here.

Keep only the relevant sections needed for analysis—avoid uploading entire raw filings to keep the repository lightweight.
