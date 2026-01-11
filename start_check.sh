#!/bin/bash -eux

if [[ ${1:-} == "--full" ]]; then
  echo "[info] Running full dependency vulnerability audit (pip-audit)..."
  uv run pip-audit
else
  echo "[info] Tip: Run with --full to include dependency vulnerability audit (pip-audit)."
fi

./scripts/check_test_files.sh

uv run ruff check src/ tests/

uv run ruff format --diff src/ tests/

uv run pyright src/ tests/

uv run bandit -r src/

echo "[info] All checks completed. If you see no errors above, your codebase is clean!"
