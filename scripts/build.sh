#!/usr/bin/env sh
set -eu

if [ -n "${LS_LATEX_PYTHON:-}" ]; then
  if "$LS_LATEX_PYTHON" -c 'import sys; raise SystemExit(sys.version_info < (3, 9))'; then
    exec "$LS_LATEX_PYTHON" "$(dirname "$0")/build.py" "$@"
  fi
fi

for candidate in python3 python3.14 python3.13 python3.12 python3.11 python3.10 python3.9 python; do
  if command -v "$candidate" >/dev/null 2>&1 \
    && "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 9))'; then
    exec "$candidate" "$(dirname "$0")/build.py" "$@"
  fi
done

echo "Python 3.9 or newer was not found." >&2
exit 1
