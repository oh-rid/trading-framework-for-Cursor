# Economic Indicators Data

This folder stores JSON or CSV snapshots produced by the indicator-collection utilities in `tools/indicators/` (e.g., `collect_indicators.py`).

Typical files include:

- Time-stamped JSON dumps of macroeconomic or market indicators
- CSV tables aligned for back-testing or dashboard ingestion

Files are usually named with an ISO date to make versioning explicit. Avoid committing very large raw datasets; trim to the fields needed for analysis and visualization.
