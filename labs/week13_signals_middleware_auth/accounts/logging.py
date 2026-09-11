"""Structured JSON Logging Engine with Distributed Trace Correlation.

Provides:
- ContextVar-based trace propagation across async/sync thread boundaries.
- RFC 3339 UTC timestamps and standardized observability schemas.
- TraceContextMiddleware to bind incoming HTTP headers (X-Trace-ID, X-Request-ID).
"""

from __future__ import annotations

from contextvars import ContextVar
from datetime import datetime, timezone
import json
import logging
from typing import Any
import uuid

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

# Context storage for correlation across call boundaries
trace_id_ctx: ContextVar[str] = ContextVar("trace_id", default="")
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

_RESERVED_ATTRS = {
    "args", "asctime", "created", "exc_info", "exc_text", "filename",
    "funcName", "levelname", "levelno", "lineno", "module", "msecs",
    "message", "msg", "name", "pathname", "process", "processName",
    "relativeCreated", "stack_info", "thread", "threadName", "taskName",
}


def set_trace_context(trace_id: str | None = None, request_id: str | None = None) -> None:
    """Set the active trace and request identifiers in the current context."""
    trace_id_ctx.set(trace_id or uuid.uuid4().hex)
    request_id_ctx.set(request_id or uuid.uuid4().hex)


def clear_trace_context() -> None:
    """Reset trace identifiers."""
    trace_id_ctx.set("")
    request_id_ctx.set("")


class StructuredJSONFormatter(logging.Formatter):
    """Formats log records as production-grade JSON with trace correlation context."""

    def format(self, record: logging.LogRecord) -> str:
        trace_id = trace_id_ctx.get() or getattr(record, "trace_id", None) or "none"
        request_id = request_id_ctx.get() or getattr(record, "request_id", None) or "none"

        log_payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": trace_id,
            "request_id": request_id,
            "source": f"{record.module}:{record.lineno}",
            "function": record.funcName,
        }

        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        # Append custom 'extra' parameters safely
        for key, value in record.__dict__.items():
            if key not in _RESERVED_ATTRS and not key.startswith("_"):
                try:
                    json.dumps(value)  # Check serializability
                    log_payload[key] = value
                except (TypeError, OverflowError):
                    log_payload[key] = str(value)

        return json.dumps(log_payload)


class TraceContextMiddleware(MiddlewareMixin):
    """Intercepts request to seed trace correlation context from headers or generate new."""

    def process_request(self, request: HttpRequest) -> None:
        trace_id = (
            request.headers.get("X-Trace-ID")
            or request.headers.get("traceparent")
            or uuid.uuid4().hex
        )
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex

        set_trace_context(trace_id=trace_id, request_id=request_id)
        request.trace_id = trace_id  # type: ignore[attr-defined]
        request.request_id = request_id  # type: ignore[attr-defined]

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        trace_id = trace_id_ctx.get()
        request_id = request_id_ctx.get()

        if trace_id:
            response["X-Trace-ID"] = trace_id
        if request_id:
            response["X-Request-ID"] = request_id

        return response
