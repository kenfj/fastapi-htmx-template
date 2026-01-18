## syntax=docker/dockerfile:1.4

FROM ghcr.io/astral-sh/uv:0.9.24 AS uv_bin

## ===== builder stage: production dependencies only =====
FROM python:3.14-slim AS builder
COPY --from=uv_bin /uv /uvx /bin/

WORKDIR /app

# https://docs.astral.sh/uv/guides/integration/docker/#optimizations
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
	--mount=type=bind,source=uv.lock,target=uv.lock \
	--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
	uv sync --locked --no-install-project


## ===== tester stage: dev dependencies + tests =====
FROM python:3.14-slim AS tester
COPY --from=uv_bin /uv /uvx /bin/

RUN apt-get update && apt-get install -y libatomic1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

ENV APP_ENV=test
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked

RUN ./start_check.sh && uv run pytest --maxfail=1 --disable-warnings -q


## ===== prod stage: production dependencies + app code only =====
FROM python:3.14-slim AS runtime
COPY --from=uv_bin /uv /uvx /bin/

WORKDIR /app

## Copy entire venv from builder for full activation
COPY --from=builder /app/.venv /app/.venv

## Copy only required app code from tester (exclude tests etc)
COPY --from=tester /app/src /app/src
COPY --from=tester /app/static /app/static
COPY --from=tester /app/data /app/data
COPY --from=tester /app/.env* /app/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=src
ENV VIRTUAL_ENV=/app/.venv

EXPOSE 8000
CMD ["fastapi", "run", "./src/main.py"]
