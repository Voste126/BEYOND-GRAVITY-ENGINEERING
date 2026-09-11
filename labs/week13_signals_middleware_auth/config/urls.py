"""Root URL configuration — minimal, just for middleware testing."""

from django.http import JsonResponse
from django.urls import path


def health_check(request):  # noqa: ANN001, ANN201
    """Simple endpoint for middleware tests to hit."""
    org = getattr(request, "organization", None)
    return JsonResponse({
        "status": "ok",
        "organization": org.slug if org else None,
    })


urlpatterns = [
    path("health/", health_check, name="health-check"),
]
