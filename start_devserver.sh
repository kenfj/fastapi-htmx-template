#!/bin/bash

export APP_ENV=development
uv run fastapi dev ./src/main.py
