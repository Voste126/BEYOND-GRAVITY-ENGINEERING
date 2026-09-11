"""Events app models — carried forward from Week 11 + new stubs for Week 13.

``LaunchEvent`` fields are PROVIDED (working code from Month 3).
``LaunchEvent.save()`` override and ``AuditLog`` model are STUBS — implement them.
"""

from __future__ import annotations

from typing import Any

from django.db import models


# ---------------------------------------------------------------------------
# CARRY-FORWARD: LaunchEvent (fields provided from Week 11)
# ---------------------------------------------------------------------------


class LaunchEvent(models.Model):
    """A launch-event domain entity stored in the database.

    Fields are provided — you implemented these in Week 11.
    """

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("launched", "Launched"),
        ("scrubbed", "Scrubbed"),
    ]

    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "events"

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"

    # --- STUB: Override save() to fire signals (Task 1) --------------------

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override to detect status changes and fire custom signals.

        Steps:
        1. If ``self.pk`` is not None, query the DB for the current
           (pre-save) status.  Store it as ``old_status``.
        2. Call ``super().save(*args, **kwargs)``.
        3. If this is a NEW instance (no prior pk) and ``status == "scheduled"``,
           send ``event_scheduled`` signal.
        4. If ``old_status`` exists and differs from ``self.status``,
           send ``event_status_changed`` signal with ``old_status`` and
           ``new_status`` kwargs.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# STUB: AuditLog model (Task 1)
# ---------------------------------------------------------------------------


class AuditLog(models.Model):
    """Records significant lifecycle events for audit purposes.

    STUB: Add these fields:
        event: ForeignKey to ``LaunchEvent`` (CASCADE on delete).
        action: CharField(max_length=50) — e.g. ``"SCHEDULED"``, ``"STATUS_CHANGED"``.
        details: TextField — human-readable description.
        created_at: DateTimeField(auto_now_add=True).
    """

    # TODO: add fields here
    #   event = models.ForeignKey(LaunchEvent, ...)
    #   action = models.CharField(...)
    #   details = models.TextField(...)
    #   created_at = models.DateTimeField(...)

    class Meta:
        app_label = "events"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        raise NotImplementedError
