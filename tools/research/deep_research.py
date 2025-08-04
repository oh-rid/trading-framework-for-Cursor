#!/usr/bin/env python3
"""tools/research/deep_research.py

CLI tool for running deep research on a ticker using OpenAI.

Usage:
    python tools/research/deep_research.py AAPL "Explain the key revenue growth drivers"
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
import re

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# Path to the system prompt
PROMPT_FILE = Path(__file__).with_suffix("").parent / "prompts" / "multi_agent.md"
DEFAULT_PROMPT_FILE = Path(__file__).with_suffix("").parent / "prompts" / "default.md"


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Deep research via GPT-4o-mini; Markdown output to file",
    )
    parser.add_argument(
        "ticker",
        nargs="?",
        default="GENERAL",
        help="Stock ticker (optional). Defaults to 'GENERAL' if omitted.",
    )
    parser.add_argument(
        "prompt",
        nargs=argparse.REMAINDER,
        help="Prompt text for the model (required)",
    )
    return parser.parse_args()


def _init_client() -> OpenAI:
    """Create an OpenAI client, loading the key from `.env`."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment (.env)", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key)


def _ask_model(client: OpenAI, prompt: str) -> str:
    """Send prompt to the model and return the Markdown answer."""
    try:
        if PROMPT_FILE.exists():
            system_msg = PROMPT_FILE.read_text(encoding="utf-8", errors="ignore")
        elif DEFAULT_PROMPT_FILE.exists():
            system_msg = DEFAULT_PROMPT_FILE.read_text(encoding="utf-8", errors="ignore")
        else:
            system_msg = "Act as a buy-side equity research analyst. Output Markdown."

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content or ""
    except OpenAIError as err:
        print(f"OpenAI API error: {err}", file=sys.stderr)
        sys.exit(2)


def _slugify(tag: str, max_len: int = 40) -> str:
    """Clean a tag: keep alphanumerics and '-', trim to max_len."""
    slug = re.sub(r"[^A-Za-z0-9\-]+", "-", tag).strip("-")
    return slug[:max_len] or "GENERAL"


def _save_markdown(ticker: str, text: str) -> Path:
    """Save Markdown into data/deep_research/ …"""
    out_dir = Path("data/deep_research")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_tag = _slugify(ticker.upper())
    filepath = out_dir / f"{safe_tag}_{ts}.md"
    filepath.write_text(text, encoding="utf-8")
    return filepath


def main() -> None:  # noqa: D401
    args = _parse_args()
    if not args.prompt:
        print("ERROR: prompt is required", file=sys.stderr)
        sys.exit(3)

    prompt_text = " ".join(args.prompt).strip()
    client = _init_client()
    markdown = _ask_model(client, prompt_text)
    saved = _save_markdown(args.ticker, markdown)
    print(f"✔ saved → {saved}")


if __name__ == "__main__":
    main()
