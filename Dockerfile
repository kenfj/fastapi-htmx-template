## syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.14
ARG UV_VERSION=0.9.24

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_bin

FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# setup uv
COPY --from=uv_bin /uv /uvx /bin/
ENV UV_PROJECT_ENVIRONMENT="/app/.venv"
# https://docs.astral.sh/uv/guides/integration/docker/#optimizations
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy


## ===== builder stage: production dependencies only =====
FROM base AS builder

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --frozen --no-install-project --no-dev


## ===== tester stage: dev dependencies + tests =====
FROM builder AS tester

RUN apt-get update && apt-get install -y libatomic1 && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --frozen

COPY . .

# unit tests will use sqlite so APP_ENV does not matter here
ENV APP_ENV=test
RUN ./start_check.sh && uv run pytest --maxfail=1 --disable-warnings -q


## ===== e2e-tester stage: end-to-end testing dependencies =====
FROM tester AS e2e-tester

RUN uv run playwright install --with-deps chromium

COPY tests/e2e ./tests/e2e

ENV APP_ENV=test
ENV DB_HOST=host.docker.internal
ENV BASE_URL=http://host.docker.internal:8000

RUN uv run pytest tests/e2e --no-cov

## ===== runtime stage: production dependencies + app code only =====
FROM base AS runtime

RUN useradd -m appuser

## Copy entire venv from builder for full activation
COPY --from=builder /app/.venv /app/.venv

## Copy only required app code from tester (exclude tests etc)
COPY --from=tester /app/src /app/src
COPY --from=tester /app/static /app/static
COPY --from=tester /app/data /app/data
COPY --from=tester /app/.env* /app/

RUN chown -R appuser:appuser /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=src
ENV VIRTUAL_ENV=/app/.venv

USER appuser

EXPOSE 8000
CMD ["fastapi", "run", "--host", "0.0.0.0", "main:app"]
