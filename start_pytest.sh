#!/bin/bash

export APP_ENV=development

# fix snapshots with:
# uv run pytest --fix

# use pytest-watcher for automatic test running on file changes
uv run ptw --delay 3 .
