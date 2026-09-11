"""Tests for custom middleware (Task 2).

All 5 tests FAIL against the stubs.
"""

from __future__ import annotations

import pytest
from django.test import Client

from tests.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def client() -> Client:
    return Client()


# ═══════════════════════════════════════════════════════════════════════════
# RequestTimingMiddleware
# ═══════════════════════════════════════════════════════════════════════════


class TestRequestTimingMiddleware:
    """X-Request-Duration-Ms header is added to every response."""

    def test_timing_header_present(self, client: Client) -> None:
        response = client.get("/health/")
        assert "X-Request-Duration-Ms" in response.headers

    def test_timing_header_is_positive_float(self, client: Client) -> None:
        response = client.get("/health/")
        duration = float(response.headers["X-Request-Duration-Ms"])
        assert duration >= 0.0


# ═══════════════════════════════════════════════════════════════════════════
# OrganizationMiddleware
# ═══════════════════════════════════════════════════════════════════════════


class TestOrganizationMiddleware:
    """Resolves X-Organization-Slug header to an Organization instance."""

    def test_sets_organization_from_valid_slug(self, client: Client) -> None:
        org = OrganizationFactory(slug="spacex")
        response = client.get(
            "/health/",
            headers={"X-Organization-Slug": "spacex"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["organization"] == org.slug

    def test_no_header_sets_none(self, client: Client) -> None:
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["organization"] is None

    def test_invalid_slug_returns_404(self, client: Client) -> None:
        response = client.get(
            "/health/",
            headers={"X-Organization-Slug": "nonexistent"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "not found" in data["error"].lower()
