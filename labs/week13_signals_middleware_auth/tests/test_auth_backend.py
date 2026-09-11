"""Tests for custom auth backend (Task 3).

All 9 tests FAIL against the stubs.
"""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from accounts.backends import OrganizationBackend
from accounts.models import Membership
from tests.factories import MembershipFactory, OrganizationFactory, UserFactory

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture()
def backend() -> OrganizationBackend:
    return OrganizationBackend()


@pytest.fixture()
def org():  # noqa: ANN201
    return OrganizationFactory(slug="nasa")


# ═══════════════════════════════════════════════════════════════════════════
# authenticate()
# ═══════════════════════════════════════════════════════════════════════════


class TestAuthenticate:
    """Username/password authentication."""

    def test_valid_credentials(self, backend: OrganizationBackend) -> None:
        user = UserFactory(username="astro", password="s3cret!")
        result = backend.authenticate(None, username="astro", password="s3cret!")
        assert result is not None
        assert result.pk == user.pk

    def test_wrong_password_returns_none(
        self, backend: OrganizationBackend
    ) -> None:
        UserFactory(username="astro", password="s3cret!")
        result = backend.authenticate(None, username="astro", password="wrong")
        assert result is None

    def test_inactive_user_returns_none(
        self, backend: OrganizationBackend
    ) -> None:
        UserFactory(username="ghost", password="s3cret!", is_active=False)
        result = backend.authenticate(None, username="ghost", password="s3cret!")
        assert result is None


# ═══════════════════════════════════════════════════════════════════════════
# has_perm()
# ═══════════════════════════════════════════════════════════════════════════


class TestHasPerm:
    """Organisation-scoped, role-based permission checks."""

    def test_admin_can_delete(self, backend: OrganizationBackend, org) -> None:  # noqa: ANN001
        membership = MembershipFactory(
            organization=org, role=Membership.Role.ADMIN
        )
        assert backend.has_perm(
            membership.user, "events.delete_event", obj=org
        ) is True

    def test_member_cannot_delete(self, backend: OrganizationBackend, org) -> None:  # noqa: ANN001
        membership = MembershipFactory(
            organization=org, role=Membership.Role.MEMBER
        )
        assert backend.has_perm(
            membership.user, "events.delete_event", obj=org
        ) is False

    def test_viewer_can_only_view(self, backend: OrganizationBackend, org) -> None:  # noqa: ANN001
        membership = MembershipFactory(
            organization=org, role=Membership.Role.VIEWER
        )
        assert backend.has_perm(
            membership.user, "events.view_event", obj=org
        ) is True
        assert backend.has_perm(
            membership.user, "events.add_event", obj=org
        ) is False

    def test_no_membership_returns_false(
        self, backend: OrganizationBackend, org  # noqa: ANN001
    ) -> None:
        user = UserFactory()
        assert backend.has_perm(user, "events.view_event", obj=org) is False

    def test_no_org_object_returns_false(
        self, backend: OrganizationBackend
    ) -> None:
        """has_perm with obj=None should return False (no org context)."""
        user = UserFactory()
        assert backend.has_perm(user, "events.view_event", obj=None) is False


# ═══════════════════════════════════════════════════════════════════════════
# get_user()
# ═══════════════════════════════════════════════════════════════════════════


class TestGetUser:
    """User retrieval by PK."""

    def test_existing_user(self, backend: OrganizationBackend) -> None:
        user = UserFactory()
        assert backend.get_user(user.pk) == user

    def test_nonexistent_returns_none(
        self, backend: OrganizationBackend
    ) -> None:
        assert backend.get_user(99999) is None
