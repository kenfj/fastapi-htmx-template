# fastapi-htmx-template

## Pure Python Full-Stack: FastAPI × htmx × htmy — Minimal Todo App Example

> **No TypeScript, No JavaScript, No Jinja2**
> 100% Python. Type-safe, declarative HTML building and modern web app features with minimal stack.

## Project Features / Motivation

- **100% Python full-stack**: No TypeScript, JavaScript, or Jinja2 required—build everything in Python.
- **Sample app**: Minimal Todo app included as a practical example.
- **Type-safe, declarative HTML**: Use htmy to generate HTML directly in Python, with type checking and IDE support.
- **Modern, minimal stack**: FastAPI for backend, htmx for dynamic UI, Pico.css for styling, Redis for async features.
- **No SPA complexity**: Achieve dynamic, interactive UIs without the overhead of React/Vue or client-side JS frameworks.
- **Production-ready patterns**: Structured logging, async pub/sub, settings management, and testing best practices.
- **Async DB support**: Fully async connection and ORM support for both PostgreSQL and SQLite (SQLModel/SQLAlchemy async engine).
- **Easy to extend**: Clean architecture and directory structure for real-world projects and team development.

Ideal for Python developers who want to build modern web apps with minimal dependencies and no JavaScript or template engines.

---

## Directory Structure (Example)

```
.
├── src/
│   ├── main.py                # FastAPI entrypoint
│   ├── core/                  # App core (config, logger, settings, providers)
│   ├── models/                # Pydantic/SQLModel models
│   ├── services/              # Business logic, pubsub, etc.
│   ├── repositories/          # DB access layer
│   ├── routers/               # FastAPI routers
│   ├── ui/                    # htmy UI components/pages
│   ├── utils/                 # Utility functions
│   ├── enums/                 # Enum definitions
│   └── exceptions/            # Custom exceptions
├── tests/                     # Test code (mirrors src/ structure)
├── static/                    # Static files (JS, CSS)
├── data/                      # Data files (e.g. SQLite DB)
├── scripts/                   # Utility scripts
├── pyproject.toml             # Project config & dependencies
├── README.md
├── compose.yaml               # Docker Compose config
└── ... (env files, .gitignore, etc.)
```

This template follows a scalable, real-world project structure. Add your own modules, services, and features as needed.

## Tech Stack

- **FastAPI** (backend web framework)
- **SQLModel** (typed ORM, built on SQLAlchemy)
- **Pydantic v2 / pydantic-settings** (settings & validation)
- **Redis** (async pub/sub, cache, queue)
- **htmx** (dynamic frontend interactions via HTML attributes; no JS/SPA required)
- **htmy** (declarative, type-safe HTML builder for Python; no Jinja2, JS, or TS required)
- **Pico.css** (minimal CSS framework, via CDN)
- **python-json-logger** (structured logging)
- **SQLModel/SQLAlchemy async engine** (async ORM, async DB connection for PostgreSQL & SQLite)
- **pytest, pytest-asyncio, pytest-cov, inline-snapshot** (testing)
- **ruff, pyright, bandit, pip-audit** (lint/type/security/dep check)
- **uv** (modern Python package/dependency manager)

## Quick Start

```bash
# install packages
uv sync

# check codebase
./start_check.sh
./start_pytest.sh

# start docker services
docker compose up -d
docker compose ps

# start development FastAPI server
./start_devserver.sh

# Sample Todo App
open http://127.0.0.1:8000

# FastAPI Swagger docs
open http://127.0.0.1:8000/docs
```

## Dev Server in Docker Compose

```bash
# start fastapi dev server
docker compose --profile ci up -d

# up with rebuild when updated Dockerfile
docker compose --profile ci up -d --build

# start postgres and redis only for local development
docker compose up -d

# check
docker compose ps
docker compose logs -f app
```

* verify final image

```bash
docker build -t fastapi-htmx-template-prod .

# check
docker run --rm -p 8000:8000 fastapi-htmx-template-prod
docker run -it --rm fastapi-htmx-template-prod bash
```

## Upgrade Packages

```bash
# check
uv pip list --outdated

# upgrade
uv lock --upgrade
uv sync
```

## Redis Notes

```bash
# connect local redis
docker compose exec redis redis-cli

# check redis config
docker compose exec redis redis-cli CONFIG GET appendonly
```

## Reference

- Why FastAPI + SQLModel + HTMX Is My Favorite Stack in 2025
  - https://medium.com/@hadiyolworld007/why-fastapi-sqlmodel-htmx-is-my-favorite-stack-in-2025-73565aea38fc

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
