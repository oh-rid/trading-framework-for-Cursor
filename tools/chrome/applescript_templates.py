"""AppleScript template generators for Google Chrome automation.

These helpers return AppleScript source strings that can be executed via
`osascript -e` or by writing to a temporary file.

The inspiration and parts of the logic come from the dxt project:
https://github.com/anthropics/dxt/tree/main/examples/chrome-applescript

Currently implemented (MVP):
    • get_current_url_script – returns URL of active Chrome tab.

Future planned helpers (place-holders):
    • click(selector)
    • type_text(selector, text)
    • wait_for(selector)
    • extract_table_script(selector)
    • screenshot_script(selector, path)
"""
from __future__ import annotations

import textwrap

__all__ = [
    "get_current_url_script",
    "CLICK_PLACEHOLDER",  # to avoid flake warnings until implemented
]


def get_current_url_script() -> str:
    """Return AppleScript that prints the URL of the active tab."""
    # Using Google Chrome AppleScript dictionary.
    # `return` passes result to stdout when executed with `osascript`.
    return textwrap.dedent(
        """
        tell application \"Google Chrome\"
            set theUrl to URL of active tab of front window
        end tell
        return theUrl
        """
    ).strip()


# ---------------------------------------------------------------------------
# TODO place-holders below. They will be implemented as we expand features.
# ---------------------------------------------------------------------------

def CLICK_PLACEHOLDER() -> None:  # pragma: no cover
    """Stub so that the module exports something else besides the first function."""
    raise NotImplementedError 