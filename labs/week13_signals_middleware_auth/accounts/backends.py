"""Custom authentication backend (Task 3 — STUB).

Implement ``OrganizationBackend`` with three methods:

1. ``authenticate(self, request, username=None, password=None, **kwargs)``
   - Look up User by username, call ``check_password()``.
   - Return ``None`` if user doesn't exist, password is wrong,
     or ``user.is_active`` is False.
   - Return the ``User`` on success.

2. ``has_perm(self, user_obj, perm, obj=None)``
   - If ``obj`` is not an ``Organization`` instance, return ``False``.
   - Look up the user's ``Membership`` in that org.
   - Check ``perm`` against ``ROLE_PERMISSIONS[membership.role]``.
   - Return ``False`` if no membership exists.

3. ``get_user(self, user_id)``
   - Return ``User`` by pk, or ``None`` if not found.

Permission matrix (define as ``ROLE_PERMISSIONS`` class attribute):
    viewer:  {"events.view_event"}
    member:  {"events.view_event", "events.add_event", "events.change_event"}
    admin:   {"events.view_event", "events.add_event", "events.change_event",
              "events.delete_event", "events.manage_members"}
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model  # noqa: F401
from django.http import HttpRequest  # noqa: F401

User = get_user_model()


class OrganizationBackend:
    """Org-scoped, role-based authentication backend."""

    ROLE_PERMISSIONS: dict[str, set[str]] = {
        "viewer": {"events.view_event"},
        "member": {"events.view_event", "events.add_event", "events.change_event"},
        "admin": {
            "events.view_event",
            "events.add_event",
            "events.change_event",
            "events.delete_event",
            "events.manage_members",
        },
    }

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Authenticate by username + password.

        Returns the User on success, None on failure.
        """
        raise NotImplementedError

    def has_perm(self, user_obj: Any, perm: str, obj: Any = None) -> bool:
        """Check org-scoped permission.

        ``obj`` must be an ``Organization`` instance for this backend
        to return ``True``.
        """
        raise NotImplementedError

    def get_user(self, user_id: int) -> Any:
        """Return User by pk, or None."""
        raise NotImplementedError
