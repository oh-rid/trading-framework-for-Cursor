# data/

Raw input files live here. Nothing inside this folder is tracked by Git (see `.gitignore`) so feel free to drop large CSV, JSON or images without worrying about repo bloat.

Typical sub-folders:

| Sub-folder | Purpose |
|-----------|---------|
| `indicators/` | Daily/weekly dumps collected by `tools/indicators` |
| `portfolio/`  | CSV exports from IBKR Portfolio Analyst |
| `sec_data/`   | SEC risk-factor markdown files fetched by `tools/sec` |
| `backtests/`  | CSV & PNG outputs produced by back-testing scripts |
| `youtube/` / `books/` | Any external datasets you want to experiment with |

Feel free to add more directories as your workflow evolves. The only rule: **keep raw, unprocessed data in `data/`, put AI-ready distillates into `knowledge/`.**
