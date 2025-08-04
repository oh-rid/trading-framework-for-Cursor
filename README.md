# AI-first Trading Framework for Cursor 

<p align="center">
  <img src="Bonus.png" alt="AI Trading OS Overview" width="600"/>
</p>

This project is a **semi-manual framework for managing a personal Brokerage Account (Interactive Brokers in example)**.

It is intentionally simple: you still think and learn at every step, while the assistant helps with the heavy lifting.

---

### 🗂️ Folder Map

- **data/** – raw data landing zone. Drop files manually or collect them automatically with the tools.
- **knowledge/** – AI-ready distillates (token-optimised) produced by prompt workflows.
- **memory_bank/** – hand-picked knowledge you want the agent to remember. See its README for structure.
- **tools/** – scripts the chat agent can call to fetch context, analyse an idea or even place an order in TWS.
- **prompts/** – reusable prompt templates that standardise recurring processes.
- **learning/** – notes produced via the *learning* prompt for the human side of the workflow.

> Sample JSON, CSV and Markdown files are provided purely for learning and experimentation. Replace them with your own data when ready.

### 🔄 Typical Usage Flows

1. **Collect → Distil → Ask**  
   Gather fresh data (or let the tools do it), convert it into knowledge distillates, learn yourself *and* feed the agent. Then ask portfolio or idea questions.
2. **Decide → Execute → Log**  
   When you like an idea, ask the agent to execute via tools/TWS, then append the order to the trade journal in *memory_bank*.
3. **Reflect**  
   Review winning/losing ideas and update the knowledge base accordingly.
4. **Code & Extend**  
   Add new tools, automate the memory bank or create an ideas folder – the framework is yours to evolve.
5. **Reflect & Automate**  
   Design your own reflection loop: review outcomes, update distillates, and gradually automate any repetitive steps that are currently triggered manually in chat.

## ❓ Why Semi-Manual?
1. Learning by doing – you touch the raw data, prompts and code.  
2. Full visibility – every stage of the investment workflow is explicit; nothing happens behind the curtain.

## 🎛️ Context Switches
The assistant can operate in four high-level contexts:

| Context | Purpose |
|---------|---------|
| **analysis** | Explore data, run deep research prompts, interpret indicators. |
| **execution** | Call tools (IBRK, Bybit, SEC, indicators) and perform actions that change state. |
| **reflection** | Write trade-journal entries, update mindsets, review decisions. |
| **coding** | Extend or modify the utilities inside `tools/` (new collectors, CLI wrappers, etc.). |

Switching context is implicit: the assistant infers the mode from your request. You can force it, e.g. “switch to coding context”.

## 🧠 Memory Model
Active knowledge is loaded automatically from `memory_bank/active_memory/` on every assistant run.

| Folder | What to copy (manually or via ChatGPT) |
|--------|----------------------------------------|
| `indicators/` | Latest JSON dump from `tools/indicators` |
| `portfolio/`  | Fresh portfolio CSV exported from IBKR |
| `mindset/`    | Current mindset / frameworks markdowns |
| `trade_journal/` | When you **decide** to buy/sell, ask ChatGPT to append a record here – this will power the reflection module in v2 (bring popcorn). |

> Files are **NOT** moved automatically – copy them yourself or instruct the chat to do so when appropriate.
>
> **Sample data included:** Several JSON, CSV and Markdown files in the repo are *example snapshots* left intentionally for learning and demonstration purposes (e.g. indicator dumps, portfolio exports, mindset distillates). Feel free to explore or replace them with your own real data.

---

---

## 🚀 Quick-Start Cheat-Sheet

```bash
# 0.  Activate virtualenv + load secrets
source .venv/bin/activate      # VS Code should auto-activate thanks to .vscode/settings.json
cp env.example .env               # first run only; then edit .env and add BYBIT_API_KEY, FRED_API_KEY, etc.


# 1.  Collect fresh data (Collect)
# Put reference PDFs into data/books/ for later summarisation
python tools/indicators/collect_indicators.py --out data/indicators/          # macro/liquidity
python tools/IBRK/export_portfolio.py --host localhost --port 7497 \          # portfolio snapshot
       --out data/portfolio/positions_$(date +%F_%H-%M)_full.csv
python tools/sec/secctl.py fetch --ticker AMD --section RiskFactors \         # SEC risk factors
       --out data/sec_data/

# 2.  Distil into knowledge (Distil)
#     – ask the chat agent to run the appropriate prompt on new data using prompts

# 3.  Explore / decide (Ask & Decide)
streamlit run tools/dashboard/dashboard.py                                    # visual overview
python tools/backtest/backtestctl.py run config/reit_strategy.yaml            # sandbox back-test

# 4.  Execute & log (Execute → Log)
#     – via chat: place_order / log to memory_bank/trade_journal
```


For detailed documentation of each utility see `tools/README.md`.

> ⚠️ **Model choice matters**
> 
> Use the **o3** model in the Cursor chat. At the time of building this framework it scored best in financial reasoning tests.  