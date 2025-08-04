#!/usr/bin/env python3
"""CLI tool to automate Google Chrome via AppleScript.

Usage:
    python tools/chrome/chromectl.py --profile generic --action get_current_url

This MVP supports only the *generic* profile with the *get_current_url* action.
Further actions will be added incrementally.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

# Attempt relative import (when run as module) and fallback (when run as script)
try:
    from . import applescript_templates as templates  # type: ignore
except ImportError:  # pragma: no cover – fallback for "python chromectl.py"
    import importlib.util
    from pathlib import Path as _Path

    _module_path = _Path(__file__).parent / "applescript_templates.py"
    _spec = importlib.util.spec_from_file_location("applescript_templates", _module_path)
    if _spec and _spec.loader:
        templates = importlib.util.module_from_spec(_spec)  # type: ignore
        _spec.loader.exec_module(templates)  # type: ignore
    else:
        raise

ROOT_DIR = Path(__file__).resolve().parents[2]  # project root
PROFILES_DIR = Path(__file__).resolve().parent / "profiles"


class ProfileError(RuntimeError):
    """Raised when profile or action is invalid."""


def load_profile(profile_name: str) -> Dict[str, Any]:
    """Load YAML profile from tools/chrome/profiles/{profile_name}.yaml."""
    profile_path = PROFILES_DIR / f"{profile_name}.yaml"
    if not profile_path.exists():
        raise ProfileError(f"Profile '{profile_name}' not found at {profile_path}")

    with profile_path.open("r", encoding="utf-8") as fh:
        try:
            return yaml.safe_load(fh) or {}
        except yaml.YAMLError as exc:
            raise ProfileError(f"Failed to parse YAML in {profile_path}: {exc}")


def read_keychain(service: str) -> str | None:  # pragma: no cover
    """Return password/login string from macOS Keychain or None if not found."""
    try:
        return (
            subprocess.check_output(["security", "find-generic-password", "-s", service, "-w"], text=True)
            .strip()
        )
    except subprocess.CalledProcessError:
        return None


def build_applescript(profile_data: Dict[str, Any], action_name: str) -> Tuple[str, Optional[str], Optional[str]]:
    """Generate AppleScript for the requested action.

    Currently implemented actions:
        • get_current_url (generic profile)
    """
    actions = profile_data.get("actions", {})
    if action_name not in actions:
        raise ProfileError(f"Action '{action_name}' not defined in profile")

    action_cfg = actions[action_name] or {}

    js_cmds: list[str] = []
    wait_blocks: list[list[str]] = []

    # 1. Navigate if needed (for action itself)
    if url := action_cfg.get("navigate"):
        js_cmds.append(templates.js_navigate(url))

    # 2. Login steps (always attempt; selectors may not exist -> harmless)
    login_cfg = profile_data.get("login") or {}
    success_sel = login_cfg.get("success_selector")

    # We will only focus/click fields; no automatic typing.
    for step in login_cfg.get("steps", []):
        stype = step.get("type")
        selector = step.get("selector")
        if not selector:
            continue
        if stype in ("click", "text"):
            # Just click to focus; user will type manually if needed
            js_cmds.append(templates.js_click(selector))
        elif stype == "wait_for":
            wait_blocks.append(templates.wait_for_block(selector))

    # 3. Build AppleScript for pre-steps
    extract_table_selector = None
    extract_format = None

    extract_conf = action_cfg.get("extract")
    if extract_conf == "location":
        # We can just run separate get_current_url_script after executing prior JS.
        # Build AppleScript: first steps, then return URL.
        if js_cmds:
            pre_script = templates.build_applescript_from_js(js_cmds)
            script = pre_script + "\n" + templates.get_current_url_script()
        else:
            script = templates.get_current_url_script()

        # If success_selector defined, wrap logic to prompt user
        if success_sel:
            pre_script = pre_script  if js_cmds else ""
            # leave script building after loop
        # We'll return assembled after prompting
        return script, success_sel, None
    elif extract_conf == "html":
        # Return full HTML for post-processing
        pre_script = templates.build_applescript_from_js(js_cmds) if js_cmds else ""
        full_script = pre_script + "\n" + templates.get_html_script()
        return full_script, success_sel, "HTML"
    elif isinstance(extract_conf, dict) and extract_conf.get("table_selector"):
        extract_table_selector = extract_conf.get("table_selector")
        extract_format = extract_conf.get("format", "csv")

        if extract_format != "csv":
            raise ProfileError("Only CSV format is supported for now")

        # Build AppleScript: pre steps + extraction script
        pre_script = ""
        if js_cmds or wait_blocks:
            pre_script = templates.build_applescript_from_js(js_cmds)
            # Insert wait_blocks before closing end tell
            if wait_blocks:
                lines = pre_script.split("\n")
                # insert before 'end tell'
                end_idx = lines.index('end tell')
                insert_lines = [l for block in wait_blocks for l in block]
                lines[end_idx:end_idx] = insert_lines
                pre_script = "\n".join(lines)

        extraction_script = templates.table_to_csv_script(extract_table_selector)
        full_script = pre_script + "\n" + extraction_script if pre_script else extraction_script
        return full_script, success_sel, extract_table_selector
    else:
        raise ProfileError("Unsupported action configuration in profile")


def run_applescript(script: str) -> str:
    """Execute AppleScript source and return stdout."""
    # Use osascript with -e so we don't write temp files.
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("osascript not found. Are you on macOS?")
    except subprocess.CalledProcessError as exc:
        err = exc.stderr.strip()
        raise RuntimeError(f"AppleScript execution failed: {err}") from exc


def ensure_logged_in(success_selector: str) -> None:
    """Prompt user to log in until success_selector appears."""
    while True:
        presence_script = templates.selector_presence_script(success_selector)
        res = run_applescript(presence_script)
        if res.lower() == "true":
            return
        input(
            "It looks like you are not logged in yet. Please log in via the browser, then press Enter to re-check..."
        )
        time.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automate Google Chrome via AppleScript")
    parser.add_argument("--profile", required=True, help="YAML profile name (without .yaml)")
    parser.add_argument("--action", required=True, help="Action defined in the profile")
    args = parser.parse_args()

    try:
        profile_data = load_profile(args.profile)
        script, success_sel, data_type = build_applescript(profile_data, args.action)

        # If login required, prompt user first
        if success_sel:
            ensure_logged_in(success_sel)

        output = run_applescript(script)

        # Save results if any and table selector was involved or generic output
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_dir = ROOT_DIR / "data" / "chrome"
        save_dir.mkdir(parents=True, exist_ok=True)

        if data_type == "HTML":
            filename = f"{args.profile}_{args.action}_{timestamp}.html"
            out_path = save_dir / filename
            out_path.write_text(output, encoding="utf-8")

            # Parse headlines automatically
            try:
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(output, "html.parser")
                headlines = []
                seen = set()
                for tag in ["h1", "h2", "h3"]:
                    for el in soup.find_all(tag):
                        txt = el.get_text(strip=True)
                        if txt and txt not in seen:
                            seen.add(txt)
                            headlines.append(txt)
                        if len(headlines) >= 5:
                            break
                    if len(headlines) >= 5:
                        break
                hl_path = save_dir / f"{args.profile}_{args.action}_{timestamp}_headlines.txt"
                hl_path.write_text("\n".join(headlines), encoding="utf-8")
                print("Заголовки:\n" + "\n".join(headlines))
                print(f"HTML сохранён в {out_path}\nHeadlines сохранены в {hl_path}")
            except Exception as ex:
                print(f"Не удалось распарсить заголовки: {ex}")
                print(f"HTML сохранён в {out_path}")
        elif data_type and data_type.endswith("csv"):
            filename = f"{args.profile}_{args.action}_{timestamp}.csv"
            out_path = save_dir / filename
            out_path.write_text(output, encoding="utf-8")
            print(f"CSV сохранён в {out_path}")
        else:
            # For simple location extraction save to txt for consistency
            filename = f"{args.profile}_{args.action}_{timestamp}.txt"
            out_path = save_dir / filename
            out_path.write_text(output, encoding="utf-8")
            print(output)
            print(f"Результат также сохранён в {out_path}")
    except ProfileError as pe:
        print(f"Profile error: {pe}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # broad catch – improve later
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 