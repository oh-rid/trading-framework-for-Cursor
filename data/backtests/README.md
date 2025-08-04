# Backtests

The sample CSV/PNG files in this folder come from a **toy back-tester** shipped with the repo. The script is fine for quick sandbox checks, but it is *not* a production-grade engine.

For robust research you may prefer to:

1. Build a proper integration with a dedicated back-testing API / platform (e.g. QuantConnect, Backtrader, Zipline, PyFolio).  
2. Export well-prepared CSVs and load them directly into Interactive Brokers TWS for strategy testing — IB's own environment gives the most accurate fills/commissions.

Feel free to keep the lightweight script for experimentation, but rely on professional tools before putting real money at risk.