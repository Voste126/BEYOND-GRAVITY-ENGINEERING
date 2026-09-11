"""Accounts models (Task 3 — STUB).

Implement two models:

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

   Role choices (use ``models.TextChoices``):
       VIEWER  = "viewer"
       MEMBER  = "member"
       ADMIN   = "admin"
"""

from __future__ import annotations

from django.conf import settings  # noqa: F401
from django.db import models


class Organization(models.Model):
    """An organisation that owns launch events.

    STUB: Add ``name`` and ``slug`` fields, and implement ``__str__``.
    """

    # TODO: add fields here
    #   name = models.CharField(...)
    #   slug = models.SlugField(...)

    class Meta:
        app_label = "accounts"

    def __str__(self) -> str:
        raise NotImplementedError


class Membership(models.Model):
    """Links a User to an Organisation with a role.

    STUB: Add ``user``, ``organization``, and ``role`` fields.
    """

    class Role(models.TextChoices):
        VIEWER = "viewer", "Viewer"
        MEMBER = "member", "Member"
        ADMIN = "admin", "Admin"

    # TODO: add fields here
    #   user = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    #   organization = models.ForeignKey(Organization, ...)
    #   role = models.CharField(...)

    class Meta:
        app_label = "accounts"
        # TODO: add unique_together = ("user", "organization")

    def __str__(self) -> str:
        raise NotImplementedError
