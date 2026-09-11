"""Signal receivers for the events app (Task 1 — STUB).

Connect handlers to the custom signals defined in ``events.signals``.
Use the ``@receiver`` decorator from ``django.dispatch``.

Receivers:
1. ``log_event_scheduled`` — listens to ``event_scheduled``.
   Creates an ``AuditLog`` with:
       action="SCHEDULED"
       event=instance
       details=f"Event '{instance.name}' scheduled"

2. ``log_status_change`` — listens to ``event_status_changed``.
   Creates an ``AuditLog`` with:
       action="STATUS_CHANGED"
       event=instance
       details=f"Status changed from '{old_status}' to '{new_status}'"
"""

from __future__ import annotations

# TODO: implement receivers here
# from django.dispatch import receiver
# from events.models import AuditLog
# from events.signals import event_scheduled, event_status_changed
#
# @receiver(event_scheduled)
# def log_event_scheduled(sender, instance, **kwargs):
#     ...
#
# @receiver(event_status_changed)
# def log_status_change(sender, instance, old_status, new_status, **kwargs):
#     ...
