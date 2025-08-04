#!/usr/bin/env python
"""
researchctl.py – thin wrapper for deep_research.py

Usage:
    ./tools/research/researchctl.py <tag> "question …"

• Loads OPENAI_API_KEY via python-dotenv (.env in project root).
• Forwards the tag + question to deep_research.py, using the *same*
  Python executable that is running this file (guaranteed venv).
• After the child script finishes, finds the newest Markdown file
  in data/deep_research/ matching this tag and prints its relative
  path – so Cursor turns it into a clickable link.
"""

from __future__ import annotations
import subprocess, sys, pathlib, re
from dotenv import load_dotenv

# ────────────────── config ──────────────────
ROOT = pathlib.Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")                       # reads OPENAI_API_KEY

OUT_DIR = ROOT / "data" / "deep_research"
SCRIPT   = pathlib.Path(__file__).with_name("deep_research.py")

# ─────────────────── util ────────────────────

def slugify(text: str) -> str:
    """Simple slug for glob-matching filenames."""
    return re.sub(r"[^a-zA-Z0-9\-]+", "-", text.lower()).strip("-")[:40]

# ─────────────────── main ────────────────────

def main() -> None:
    if len(sys.argv) < 3:
        sys.exit("usage: researchctl.py <tag> <question …>")
    tag, *q = sys.argv[1:]
    question = " ".join(q)

    # run deep_research.py in the same venv
    cmd = [sys.executable, str(SCRIPT), tag, question]
    subprocess.run(cmd, check=True)

    # locate the newest .md file for this tag
    pattern = f"{slugify(tag)}_*.md"
    try:
        latest = max(OUT_DIR.glob(pattern))
        print(latest.relative_to(pathlib.Path.cwd()))
    except ValueError:
        sys.exit(f"No output file matching {pattern}")

if __name__ == "__main__":
    main()
