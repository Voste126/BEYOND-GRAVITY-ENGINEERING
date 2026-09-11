"""Custom Django signals for the events app (Task 1 — STUB).

Define two signals here:

1. ``event_scheduled`` — sent when a LaunchEvent is created with
   status="scheduled".  Provides: sender, instance.

2. ``event_status_changed`` — sent when a LaunchEvent's status field
   changes on update.  Provides: sender, instance, old_status, new_status.

Use ``django.dispatch.Signal()`` to create each signal.
"""

from __future__ import annotations

import django.dispatch

# TODO: define these signals
# event_scheduled = django.dispatch.Signal()
# event_status_changed = django.dispatch.Signal()

# Temporary placeholders so imports don't break — replace with real signals
event_scheduled = None  # type: ignore[assignment]
event_status_changed = None  # type: ignore[assignment]
