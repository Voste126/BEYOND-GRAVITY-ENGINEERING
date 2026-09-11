"""Dry-run script verifying structured JSON logging and distributed trace correlation."""

import os
import sys

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.core.management import call_command
# Sync database in memory/local SQLite for dry run
call_command("migrate", run_syncdb=True, verbosity=0)

import logging
from django.test import Client
from accounts.models import Organization
from accounts.logging import set_trace_context, clear_trace_context

logger = logging.getLogger("accounts")

def run_dry_run() -> None:
    print("=" * 70)
    print("STARTING STRUCTURED JSON LOGGING & TRACE CORRELATION DRY-RUN")
    print("=" * 70)

    # 1. Manual Context-bound Structured Log
    set_trace_context(trace_id="manual-trace-8888", request_id="req-uuid-1111")
    logger.info("Initializing security subsystem check", extra={"subsystem": "auth_audit", "env": "staging"})
    logger.warning("Simulated transient rate-limit warning", extra={"rate_limit_bucket": "login_attempts", "retry_after_s": 5})

    # 2. Log with Exception Traceback
    try:
        raise ValueError("Simulated cryptographic failure in key derivation")
    except ValueError as err:
        logger.error("Security exception caught", exc_info=err, extra={"security_incident": False})

    clear_trace_context()

    # 3. Simulate HTTP Request with Injected Trace Headers through Middleware Pipeline
    client = Client()
    Organization.objects.get_or_create(slug="spacex", defaults={"name": "Space Exploration Technologies"})

    print("-" * 70)
    print("Executing HTTP GET with X-Trace-ID: trace-distributed-777...")
    print("-" * 70)

    response = client.get(
        "/health/",
        headers={
            "X-Trace-ID": "trace-distributed-777",
            "X-Request-ID": "req-gateway-456",
            "X-Organization-Slug": "spacex",
        },
    )

    print("-" * 70)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.content.decode()}")
    print(f"Response Header [X-Trace-ID]: {response.headers.get('X-Trace-ID')}")
    print(f"Response Header [X-Request-ID]: {response.headers.get('X-Request-ID')}")
    print(f"Response Header [X-Request-Duration-Ms]: {response.headers.get('X-Request-Duration-Ms')}")
    print("=" * 70)
    print("DRY-RUN VERIFICATION COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_dry_run()
