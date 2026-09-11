"""Custom middleware for the events app.

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

import time
from typing import Any, Callable

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin


class RequestTimingMiddleware(MiddlewareMixin):
    """Add ``X-Request-Duration-Ms`` header to every response using monotonic clock."""

    def process_request(self, request: HttpRequest) -> None:
        """Record the start time on the request object."""
        request._start_time = time.monotonic()  # type: ignore[attr-defined]

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """Calculate elapsed duration in milliseconds and add response header."""
        start_time = getattr(request, "_start_time", None)
        if start_time is not None:
            elapsed_ms = (time.monotonic() - start_time) * 1000.0
            response["X-Request-Duration-Ms"] = f"{elapsed_ms:.2f}"
        return response


class OrganizationMiddleware(MiddlewareMixin):
    """Resolve ``X-Organization-Slug`` header to an Organization instance with loose coupling."""

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse] | None = None,
        resolver: Callable[[str], Any] | None = None,
    ) -> None:
        super().__init__(get_response)
        self._resolver = resolver or self._default_resolver

    @staticmethod
    def _default_resolver(slug: str) -> Any:
        from accounts.models import Organization

        return Organization.objects.get(slug=slug)

    def process_request(self, request: HttpRequest) -> HttpResponse | None:
        """Look up org by slug header. Return None on success/absence or a 404 JsonResponse."""
        slug = request.headers.get("X-Organization-Slug")
        if not slug:
            request.organization = None  # type: ignore[attr-defined]
            return None

        try:
            org = self._resolver(slug)
            request.organization = org  # type: ignore[attr-defined]
            return None
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Organization not found"}, status=404)
        except Exception:
            return JsonResponse({"error": "Organization not found"}, status=404)
