# Week 17 — Multi-stage Dockerfile (STUB)
#
# Build a production-grade Docker image for the Django app.
#
# Requirements:
#   - Two stages: "builder" and "runtime"
#   - Use python:3.12-slim as base for both
#   - Install deps with --no-cache-dir
#   - Create a non-root user "app" in runtime stage
#   - EXPOSE 8000
#   - ENTRYPOINT ["./entrypoint.sh"]
#   - CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
#
# Hints:
#   - COPY --from=builder to bring installed packages across
#   - Use /app as WORKDIR
#   - RUN addgroup/adduser to create non-root user
#   - COPY requirements.txt first (before app code) for layer caching

# ── Stage 1: Builder ──────────────────────────────────────────────────────
# TODO: implement builder stage

# ── Stage 2: Runtime ──────────────────────────────────────────────────────
# TODO: implement runtime stage
