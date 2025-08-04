# Chrome AppleScript Automation Toolkit

Utilities for automating Google Chrome on **macOS** via AppleScript. Inspired by ideas from the [anthropics/dxt](https://github.com/anthropics/dxt/tree/main/examples/chrome-applescript) project, but implemented fully in Python.

## Quick Start

```bash
pip install -r requirements.txt   # make sure PyYAML is installed

# A Chrome window must be in the foreground
python tools/chrome/chromectl.py --profile generic --action get_current_url
```

The command prints the full URL of the current tab.

## Directory Layout

```
tools/chrome/
├── chromectl.py              # CLI wrapper
├── applescript_templates.py  # AppleScript/JavaScript generators
├── profiles/
│   ├── generic.yaml          # Basic actions without login
│   └── ibkr.yaml             # Prototype profile for Interactive Brokers
└── README.md                 # this file
```

## Extending the Toolkit

1. Add new YAML profiles under `profiles/`.
2. Implement missing helpers in `applescript_templates.py` (`click`, `type_text`, `extract_table`, etc.).
3. Extend the switch logic in `chromectl.py` (the `build_applescript` function) to support new actions.

## New Features (2025-07-16)

1. **`wait_for`** — in a YAML step you can add:
   ```yaml
   - type: wait_for
     selector: "#account-summary"
   ```
   The script polls the page until the element appears (40×0.5 s).

2. **Table extraction**
   ```yaml
   actions:
     fetch_positions:
       navigate: "https://…/portfolio"
       extract:
         table_selector: "table.positions"
         format: csv  # currently only CSV
   ```
   Result saved to `data/chrome/<profile>_<action>_<ts>.csv`.

3. **Autosave results**
   • All actions write data to `data/chrome/` with a timestamp.  
   • `get_current_url` writes a `.txt`, tables result in `.csv` files.  
   • The path is printed to the console.

4. **Window screenshot (experimental)**
   ```yaml
   actions:
     snap:
       screenshot: true  # saves a PNG of the active window
   ```
   Path: `data/chrome/<profile>_<action>_<ts>.png`.

---

© 2025