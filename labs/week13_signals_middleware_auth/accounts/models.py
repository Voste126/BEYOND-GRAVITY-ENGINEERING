"""Accounts models.

1. ``Organization``
   - ``name``: CharField(max_length=255)
   - ``slug``: SlugField(unique=True)
   - ``__str__`` returns the name.

2. ``Membership``
   - ``user``: ForeignKey to ``settings.AUTH_USER_MODEL`` (CASCADE).
   - ``organization``: ForeignKey to ``Organization`` (CASCADE).
   - ``role``: CharField(max_length=20) with choices from ``Role``.
   - ``Meta.unique_together``: ``("user", "organization")``
   - ``__str__`` returns ``"<username> — <role> @ <org name>"``

   Role choices:
       VIEWER  = "viewer"
       MEMBER  = "member"
       ADMIN   = "admin"
"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class Organization(models.Model):
    """An organisation that owns launch events."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        app_label = "accounts"

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    """Links a User to an Organisation with a role."""

    class Role(models.TextChoices):
        VIEWER = "viewer", "Viewer"
        MEMBER = "member", "Member"
        ADMIN = "admin", "Admin"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )

    class Meta:
        app_label = "accounts"
        unique_together = ("user", "organization")

    def __str__(self) -> str:
        username = getattr(self.user, "username", "Unknown")
        org_name = getattr(self.organization, "name", "Unknown")
        return f"{username} — {self.role} @ {org_name}"
