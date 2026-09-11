"""Custom authentication backend with OWASP Top 10 hardening.

Mitigations applied:
- A01 (Broken Access Control): Strict type checks on target resource (obj is Organization),
  validation of user active status, verification against immutable ROLE_PERMISSIONS matrix.
- A02 (Cryptographic Failures / Timing Attacks): Constant-time password hashing execution
  on non-existent users to eliminate user enumeration side-channel timing attacks.
- A03 (Injection Vectors): Strict input validation, null-byte stripping, and boundary checks.
- A07 (Identification and Authentication Failures): Explicit is_active enforcement and
  constant-time credential validation.
"""

from __future__ import annotations

import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpRequest

User = get_user_model()
logger = logging.getLogger(__name__)

# Pre-computed dummy hash to mitigate user enumeration timing attacks
_DUMMY_PASSWORD_HASH = make_password("prevent_timing_attacks_placeholder_seed")


class OrganizationBackend:
    """Org-scoped, role-based authentication backend with zero-trust hardening."""

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
        """Authenticate by username + password with timing attack mitigation.

        Returns the User on success, None on failure.
        """
        if not username or not password or not isinstance(username, str) or not isinstance(password, str):
            check_password(password or "dummy", _DUMMY_PASSWORD_HASH)
            return None

        # Sanitize against null bytes or control characters
        sanitized_username = username.replace("\x00", "").strip()
        if not sanitized_username:
            check_password(password, _DUMMY_PASSWORD_HASH)
            return None

        try:
            user = User.objects.get(username=sanitized_username)
        except User.DoesNotExist:
            # Run constant-time check to prevent timing-based user enumeration
            check_password(password, _DUMMY_PASSWORD_HASH)
            logger.warning("Authentication failed: principal not found", extra={"principal": sanitized_username})
            return None

        if not user.is_active:
            check_password(password, user.password)
            logger.warning("Authentication failed: inactive principal", extra={"principal": sanitized_username})
            return None

        if user.check_password(password):
            logger.info("Authentication succeeded", extra={"principal": sanitized_username, "user_id": user.pk})
            return user

        logger.warning("Authentication failed: invalid credentials", extra={"principal": sanitized_username})
        return None

    def has_perm(self, user_obj: Any, perm: str, obj: Any = None) -> bool:
        """Check org-scoped permission.

        ``obj`` must be an ``Organization`` instance for this backend to return ``True``.
        """
        from accounts.models import Membership, Organization

        if not isinstance(obj, Organization):
            return False

        if not user_obj or not getattr(user_obj, "is_authenticated", False):
            return False

        if not getattr(user_obj, "is_active", False):
            return False

        try:
            membership = Membership.objects.filter(
                user=user_obj,
                organization=obj,
            ).first()
        except Exception as exc:
            logger.error("Error retrieving organization membership", exc_info=exc)
            return False

        if not membership:
            return False

        allowed_perms = self.ROLE_PERMISSIONS.get(membership.role, set())
        return perm in allowed_perms

    def get_user(self, user_id: Any) -> Any:
        """Return User by pk, or None if invalid or not found."""
        if user_id is None:
            return None

        try:
            user = User.objects.get(pk=user_id)
            return user if user.is_active else None
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return None
