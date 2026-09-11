# Week 17 — Docker & Docker Compose

## Objective

Containerise the launch-events Django app from Months 3–4 into a
production-grade Docker setup: multi-stage `Dockerfile`, a
`docker-compose.yml` with PostgreSQL + Redis, environment-driven settings,
a wait-for-dependencies entrypoint, and a `/healthz/` endpoint that
verifies every backing service.

This is the first lab where **your pass bar is infrastructure**, not just
unit tests.

---

## 🔗 Connection to Previous Months

| Artefact | How It's Used |
|----------|---------------|
| `LaunchEvent` model (Week 11) | Proves DB migrations run inside the container |
| `EventService` (Week 9) | Called from health-check to verify app layer |
| Signals + Middleware (Week 13) | Middleware runs behind Gunicorn, signals fire on model ops |
| Auth backend (Week 13) | `AUTHENTICATION_BACKENDS` wired in production settings |

---

## Tasks

### Task 1 — Multi-stage Dockerfile

Write a `Dockerfile` with two stages:

| Stage | Base Image | Purpose |
|-------|-----------|---------|
| `builder` | `python:3.12-slim` | Install build deps, copy `requirements.txt`, `pip install` |
| `runtime` | `python:3.12-slim` | Copy installed packages from builder, copy app code, create non-root user `app`, set `ENTRYPOINT` |

Requirements:
- Use `--no-cache-dir` for pip.
- Expose port **8000**.
- `ENTRYPOINT ["./entrypoint.sh"]` and `CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]`.
- The final image should run as user `app`, not root.

### Task 2 — Docker Compose

Write `docker-compose.yml` (Compose V2) with these services:

| Service | Image | Details |
|---------|-------|---------|
| `web` | Builds from `./Dockerfile` | Depends on `db` and `redis`. Env vars from `.env`. Health check: `curl -f http://localhost:8000/healthz/`. Ports: `8000:8000`. |
| `db` | `postgres:16-alpine` | Volume: `pgdata:/var/lib/postgresql/data`. Health check: `pg_isready`. Env: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`. |
| `redis` | `redis:7-alpine` | Health check: `redis-cli ping`. Port: `6379`. |

Define a named volume `pgdata`.

### Task 3 — Settings Split (12-Factor)

Split `config/settings.py` into a package:

| File | Purpose |
|------|---------|
| `config/settings/base.py` | Everything shared: `INSTALLED_APPS`, `MIDDLEWARE`, `AUTH_USER_MODEL`, `DEFAULT_AUTO_FIELD`, `TEMPLATES`. |
| `config/settings/development.py` | `DEBUG=True`, SQLite, `SECRET_KEY` hardcoded (dev only). |
| `config/settings/production.py` | `DEBUG=False`, reads `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, `ALLOWED_HOSTS` from environment. **Must raise `ImproperlyConfigured`** if `SECRET_KEY` is missing. |

### Task 4 — Entrypoint Script

Write `entrypoint.sh` that:
1. Waits for PostgreSQL to accept connections (loop with `pg_isready` or `python -c "import socket; ..."`).
2. Runs `python manage.py migrate --noinput`.
3. Runs `python manage.py collectstatic --noinput` (only if `COLLECT_STATIC=1`).
4. Executes `"$@"` (passes through CMD).

### Task 5 — Health Check Endpoint

Create a `healthcheck` app with a `/healthz/` view that:

1. Checks **database**: runs a raw SQL `SELECT 1`.
2. Checks **cache/Redis**: calls `cache.set("healthz", "ok", 1)` then `cache.get("healthz")`.
3. Returns JSON:
   - **200** when all checks pass:
     ```json
     {"status": "healthy", "checks": {"database": "up", "cache": "up"}}
     ```
   - **503** when any check fails:
     ```json
     {"status": "unhealthy", "checks": {"database": "up", "cache": "down"}}
     ```

---

## File Layout

```
labs/week17_docker_compose/
├── README.md
├── Dockerfile                   ← STUB
├── docker-compose.yml           ← STUB
├── entrypoint.sh                ← STUB
├── requirements.txt             ← provided
├── .env.example                 ← provided
├── verify.sh                    ← provided (automated pass bar checker)
├── manage.py
├── config/
│   ├── __init__.py
│   ├── wsgi.py
│   ├── urls.py                  ← provided (includes /healthz/)
│   └── settings/
│       ├── __init__.py
│       ├── base.py              ← STUB
│       ├── development.py       ← STUB
│       └── production.py        ← STUB
├── events/
│   ├── __init__.py
│   ├── apps.py
│   └── models.py                ← carry-forward (LaunchEvent)
├── healthcheck/
│   ├── __init__.py
│   ├── apps.py
│   └── views.py                 ← STUB
└── tests/
    ├── __init__.py
    ├── test_healthz.py          ← 5 pytest tests
    └── test_settings.py         ← 5 pytest tests
```

---

## How to Run

### Unit tests (no Docker needed)

```bash
cd labs/week17_docker_compose
DJANGO_SETTINGS_MODULE=config.settings.development pytest -v
```

### Full infrastructure verification

```bash
cd labs/week17_docker_compose
chmod +x verify.sh entrypoint.sh
./verify.sh
```

---

## 🎯 Pass Bar (compound)

```
1. pytest -v                                →  10 passed
2. docker compose build                     →  exit 0
3. docker compose up -d                     →  all 3 services healthy
4. curl -s http://localhost:8000/healthz/    →  {"status": "healthy", ...}
5. docker compose exec web pytest -v        →  10 passed
6. docker compose down                      →  exit 0
```

All six checks green = lab complete.
