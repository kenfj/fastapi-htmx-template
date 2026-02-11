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
- **Safe DB migrations with Flyway**: SQL-based migrations are auto-generated with Alembic and applied/managed by Flyway. Enables consistent, reviewable, and production-safe DB schema management.
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
│   ├── e2e/                   # Playwright E2E tests (features, fixtures, test_xxx.py)
│   └── unit/                  # Unit/integration tests
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
- **Playwright (Python)** (E2E browser testing; tests/e2e/)
- **ruff, pyright, bandit, pip-audit** (lint/type/security/dep check)
- **uv** (modern Python package/dependency manager)

## Quick Start

```bash
# start fastapi dev server
docker compose up -d

# start with rebuild after updated code or Dockerfile
docker compose up -d --build

# check
docker compose ps
docker compose logs -f app
```

* Sample Todo App
    * http://127.0.0.1:8000
* FastAPI Swagger docs
    * http://127.0.0.1:8000/docs
* pgAdmin
    * http://127.0.0.1:5050/
    * postgresql://app_user:app_password@postgres:5432/app_db
* RedisInsight
    * http://127.0.0.1:5540/
    * redis://default@redis:6379

## Local Development

* start `fastapi dev` on terminal and start database with docker compose
* note: local development backend server will use 127.0.0.0 for database

```bash
# install packages
uv sync

# check codebase
./start_check.sh
./start_pytest.sh
# note: pytest use sqlite in-memory database

docker compose up -d postgres redis pgadmin redisinsight

# check DB connection
psql postgres://app_user:app_password@127.0.0.1:5432/app_db
# or
export PGPASSWORD=app_password
psql -h 127.0.0.1 -p 5432 -U app_user -d app_db

# start development FastAPI server
./start_devserver.sh
```

```bash
# enable pre-commit hook (first time only)
uv run pre-commit install

# run pre-commit manually
uv run pre-commit run --all-files
```

* docker build and run manually

```bash
# start postgres and redis only for local development
docker compose up -d postgres redis

docker build -t fastapi-htmx-template .
docker run --rm -p 8000:8000 fastapi-htmx-template
docker run -it --rm fastapi-htmx-template bash
```

## DB Migration

* initial setup for alembic_version table

```bash
uv run alembic init db/migrations/alembic

uv run alembic revision -m "initial"
uv run alembic upgrade base:da33bbc9a4c2 --sql  # just for check
uv run alembic upgrade head

# make sure head in file == current in DB

uv run alembic history  # of py files in versions
# <base> -> da33bbc9a4c2 (head), initial

uv run alembic current  # of alembic_version in DB
# da33bbc9a4c2 (head)
```

* add todo table

```bash
export PYTHONPATH=src

# add py file
uv run alembic revision --autogenerate -m "add todo table"
# db/migrations/alembic/versions/2026_02_07_1927-d4cb8bc4d8e2_add_todo_table.py

uv run alembic history
# da33bbc9a4c2 -> d4cb8bc4d8e2 (head), add todo table
# <base> -> da33bbc9a4c2, initial

uv run alembic current
# da33bbc9a4c2

uv run alembic upgrade da33bbc9a4c2:head --sql | \
  grep -v alembic_version \
  > db/migrations/sql/V001__2026_02_07_1927-d4cb8bc4d8e2_add_todo_table.sql

# update DB
uv run alembic upgrade head

uv run alembic current
# d4cb8bc4d8e2 (head)
```

* run db migration manually

```bash
docker compose run --rm flyway # migrate

# use different variable (password for example)
docker compose run -e FLYWAY_PASSWORD=actual_password flyway migrate
# or
export FLYWAY_PASSWORD=actual_password
docker compose run -e FLYWAY_PASSWORD flyway migrate

# check
docker compose run --rm flyway info
docker compose run --rm flyway validate

# list tables
psql postgres://app_user:app_password@127.0.0.1:5432/app_db -c "\dt"
# or
export PGPASSWORD=password
psql -h 127.0.0.1 -p 5432 -U app_user -d app_db -c "\dt"
```

## Playwright E2E tests

```bash
# install chromium browser (~/Library/Caches/ms-playwright in Mac)
uv run playwright install --with-deps chromium

# start DB services
docker compose up -d postgres redis

# run playwright E2E locally
export APP_ENV=development
uv run pytest tests/e2e --no-cov

# run playwright E2E in container
docker build --target e2e-tester .
```

## Upgrade Packages

```bash
# check
uv pip list --outdated

# upgrade
uv lock --upgrade
uv sync
```

## SonarQube Community Locally

```bash
docker run -d --rm --name sonarqube -p 9000:9000 sonarqube:community
```

* http://127.0.0.1:9000 (admin/admin)
* Create a local project > Locally > Generate > Python > Execute the Scanner

```bash
uvx pysonar \
  --sonar-host-url=http://127.0.0.1:9000 \
  --sonar-token=<TOKEN> \
  --sonar-project-key=fastapi-htmx-template
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
