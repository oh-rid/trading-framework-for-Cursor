# Active Memory Index

This file lists the most relevant knowledge areas the system should rely on.

- mindset/
- portfolio/
- indicators/
- prompts/
- trade_journal/

**Approximate token footprint of active memory:** ~4 100 tokens

## tools/ (brief overview)
- backtest/ — strategy simulation (backtest.py, backtestctl.py)
- bybit/ — Bybit connector (bybitctl.py)
- chrome/ — managing Chrome/IBKR profiles (chromectl.py, AppleScript)
- IBRK/ — Interactive Brokers utilities (ibrkctl.py, export_portfolio.py)
- indicators/ — macro & crypto indicator collection (collect_indicators.py)
- research/ — deep research & auto-summaries (deep_research.py, researchctl.py)
- sec/ — SEC filings download & analysis (secctl.py)
- dashboard/ — Streamlit portfolio dashboard (dashboard.py, run_dashboard.sh)

## prompts/ (templates)
- book_summary_prompt_v4.1.md — extract structured distillate from books
- deep_research_multi_agent.md — multi-agent macro/position research
- deep_research_persons.md — mindset research on notable economists & traders
- learning_summary_prompt.md — distill knowledge from books into learning materials
- MERGE_books_v2.1.md — merge book distillates
- merge_persons_v1.md — merge mindset distillates
- summarize_persons_v1.md — personas short summary
