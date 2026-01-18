#!/bin/bash -e

# Checks that each src/*.py has a corresponding test file, with exclusions.

# List of src files to exclude from test existence check
EXCLUDE_FILES=(
    "src/core/providers/context.py"
    "src/core/providers/db.py"
    "src/core/providers/redis.py"
    "src/core/constants.py"
    "src/core/app_env_config.py"
    "src/core/lifespan.py"
    "src/core/logger.py"
    "src/core/settings.py"
    "src/core/types.py"
    "src/enums/app_env.py"
    "src/enums/log_format.py"
    "src/enums/log_level.py"
    "src/exceptions/not_found_error.py"
    "src/models/todo_completed_event.py"
    "src/models/todo_update.py"
    "src/utils/render.py"
    "src/main.py"
)

cd "$(dirname "$0")/.."

find src -type f -name '*.py' | while read -r srcfile; do
  if [[ "$(basename "$srcfile")" == "__init__.py" ]]; then
    continue
  fi

  skip=
  for ex in "${EXCLUDE_FILES[@]}"; do
    [[ "$srcfile" == "$ex" ]] && skip=1 && break
  done
  if [[ -n "$skip" ]]; then
    continue
  fi

  rel_path="${srcfile#src/}"
  dir="tests/$(dirname "$rel_path")"
  base="test_$(basename "$rel_path")"
  testfile="$dir/$base"

  if [[ ! -f "$testfile" ]]; then
    echo "Missing test: $testfile"
    exit 1
  fi
done

echo "All test file checks passed. No issues found."
