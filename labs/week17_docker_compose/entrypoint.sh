#!/usr/bin/env bash
# Week 17 — Container entrypoint (STUB)
#
# This script runs BEFORE the CMD (gunicorn).
#
# Implement these steps:
#   1. Wait for PostgreSQL to be ready (loop until pg_isready succeeds,
#      or use: python -c "import socket; s=socket.create_connection(('db', 5432))"
#      with retries and sleep).
#   2. Run Django migrations: python manage.py migrate --noinput
#   3. If COLLECT_STATIC=1, run: python manage.py collectstatic --noinput
#   4. Execute the CMD passed via "$@"
#
# Don't forget: set -e at the top for fail-fast behaviour.

set -e

echo "Entrypoint: starting..."

# TODO: Step 1 — wait for DB

# TODO: Step 2 — run migrations

# TODO: Step 3 — optional collectstatic

# Step 4 — hand off to CMD
exec "$@"
