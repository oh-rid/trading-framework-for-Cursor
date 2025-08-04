# Portfolio Data Snapshots

This folder contains portfolio position exports pulled from Interactive Brokers TWS.

Workflow:

1. In ChatGPT, ask the agent to run the portfolio export utility located in `tools/IBRK/export_portfolio.py` (or invoke `ibrkctl.py`).
2. The tool connects to TWS via the IB API and saves a CSV snapshot here, typically named `positions_<YYYY-MM-DD_HH-MM>_full.csv`.

> ⚠️ **Demo content** – the sample CSV in this folder is **not** the author’s real portfolio. It is provided solely as an example of the expected format. Replace it with your own export before doing any analysis.

Only keep lightweight CSV exports that are safe to share publicly. Do **not** commit sensitive account numbers or large trade-data dumps.
