#!/usr/bin/env bash
# Launch the Streamlit dashboard from project root.
# Usage: ./tools/dashboard/run_dashboard.sh [streamlit args]

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
exec "$DIR/../../.venv/bin/streamlit" run "$DIR/dashboard.py" "$@"