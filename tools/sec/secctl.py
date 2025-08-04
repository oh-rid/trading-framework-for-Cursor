#!/usr/bin/env python3
import sys, subprocess, pathlib, os
from dotenv import load_dotenv; load_dotenv()

ticker = sys.argv[1].upper()
subprocess.run([sys.executable, "tools/sec/fetch_sec.py", ticker])

try:
    dst = next(pathlib.Path("data/sec_data").glob(f"{ticker}_*_RiskFactors.md"))
except StopIteration:
    print(
        "Risk Factors file not found. Check that SEC_API_KEY is set and the fetch succeeded.",
        file=sys.stderr,
    )
    sys.exit(1)
else:
    print(dst)
