"""Custom middleware for the events app (Task 2 — STUB).

Implement two middleware classes using ``django.utils.deprecation.MiddlewareMixin``:

1. ``RequestTimingMiddleware``
   - In ``process_request``: record ``time.monotonic()`` on ``request._start_time``.
   - In ``process_response``: compute elapsed ms, add ``X-Request-Duration-Ms``
     header to the response.  Return the response.

2. ``OrganizationMiddleware``
   - In ``process_request``: read the ``X-Organization-Slug`` header.
     - If absent: set ``request.organization = None``, return ``None``.
     - If present: look up ``Organization`` by slug.
       - Found: set ``request.organization = org``, return ``None``.
       - Not found: return ``JsonResponse({"error": "Organization not found"}, status=404)``.
"""

from __future__ import annotations

from typing import Any

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RequestTimingMiddleware(MiddlewareMixin):
    """Add ``X-Request-Duration-Ms`` header to every response."""

    def process_request(self, request: HttpRequest) -> None:
        """Record the start time on the request object."""
        raise NotImplementedError

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """Calculate duration and add header."""
        raise NotImplementedError


class OrganizationMiddleware(MiddlewareMixin):
    """Resolve ``X-Organization-Slug`` header to an Organization instance."""

    def process_request(self, request: HttpRequest) -> Any:
        """Look up org by slug header. Return None or a 404 JsonResponse."""
        raise NotImplementedError
