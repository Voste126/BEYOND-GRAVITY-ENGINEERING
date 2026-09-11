# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies required for compiling C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into an isolated prefix for clean multi-stage transfer
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Hardened Zero-Trust Runtime ───────────────────────────────────────
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:${PATH}" \
    PYTHONPATH="/install/lib/python3.12/site-packages:${PYTHONPATH}"

WORKDIR /app

# Zero-trust principle: Create explicit unprivileged user and group (UID/GID 10001)
RUN groupadd -g 10001 app && \
    useradd -u 10001 -g app -s /bin/false -d /app app && \
    mkdir -p /app/run /tmp && \
    chown -R app:app /app /tmp

# Copy compiled dependencies from builder stage
COPY --from=builder /install /install

# Copy application source code with non-root ownership
COPY --chown=app:app . /app

# Ensure entrypoint execution permission
RUN chmod +x /app/entrypoint.sh

# Run as non-root user (UID 10001)
USER 10001:10001

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
