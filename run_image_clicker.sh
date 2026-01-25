#!/usr/bin/env bash
# run_image_clicker.sh
# Portable launcher for Image-Clicker(v1.2).py on Windows from bash shells (Git Bash / WSL / MSYS2)
# Usage: ./run_image_clicker.sh [args...]

# Compute script directory (the project root when this script lives next to the project files)
# This works in bash variants (Git Bash, WSL, MSYS)
# shellcheck disable=SC2034
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

# Paths relative to the script directory
PY_SCRIPT_UNIX="$SCRIPT_DIR/Image-Clicker(v1.2).py"
PY_SCRIPT_WIN="$(printf '%s' "$PY_SCRIPT_UNIX" | sed -E 's#^/([a-zA-Z])/+#\1:/#;s#/#\\\\#g')"

# Default to the unix-style path; convert to platform path when needed
PY_SCRIPT="$PY_SCRIPT_UNIX"
if [ -f /proc/version ] 2>/dev/null && grep -qi microsoft /proc/version 2>/dev/null; then
  # WSL: convert Windows-style path to WSL path if wslpath is available
  if command -v wslpath >/dev/null 2>&1; then
    PY_SCRIPT="$(wslpath -u "$PY_SCRIPT_WIN")"
  fi
elif command -v cygpath >/dev/null 2>&1; then
  # Cygwin/MSYS: convert back to unix path for these environments
  PY_SCRIPT="$(cygpath -u "$PY_SCRIPT_WIN")"
fi

# Project venv directory (relative to script location)
VENV_DIR_UNIX="$SCRIPT_DIR/venv"
VENV_DIR="$VENV_DIR_UNIX"
if [ -f /proc/version ] 2>/dev/null && grep -qi microsoft /proc/version 2>/dev/null; then
  if command -v wslpath >/dev/null 2>&1; then
    VENV_DIR="$(wslpath -u "$SCRIPT_DIR")/venv"
  fi
elif command -v cygpath >/dev/null 2>&1; then
  VENV_DIR="$(cygpath -u "$SCRIPT_DIR")/venv"
fi

# If venv exists, try to activate it and use its python
if [ -d "$VENV_DIR" ]; then
  # Typical activation script locations
  if [ -f "$VENV_DIR/bin/activate" ]; then
    # POSIX venv
    # shellcheck source=/dev/null
    . "$VENV_DIR/bin/activate"
    PYTHON_CMD=${PYTHON_CMD:-python}
  elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    # MSYS/Cygwin Git Bash may still use Scripts/activate
    . "$VENV_DIR/Scripts/activate"
    PYTHON_CMD=${PYTHON_CMD:-python}
  else
    PYTHON_CMD=${PYTHON_CMD:-python}
  fi
else
  # fallback to env override or system python
  PYTHON_CMD=${PYTHON_CMD:-python}
fi

# Run
exec "$PYTHON_CMD" "$PY_SCRIPT" "$@"
