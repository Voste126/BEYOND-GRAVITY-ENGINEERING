"""Tests for custom Django signals and audit logging (Task 1).

All 7 tests FAIL against the stubs.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from events.models import AuditLog, LaunchEvent
from events.signals import event_scheduled, event_status_changed
from tests.factories import LaunchEventFactory

pytestmark = pytest.mark.django_db


# ── signal spy fixture ─────────────────────────────────────────────────────


@pytest.fixture()
def signal_spy():
    """Return a factory that connects a mock handler to a signal and returns it."""

    connected: list[tuple] = []

    def _connect(signal):  # noqa: ANN001, ANN202
        handler = MagicMock()
        signal.connect(handler, weak=False)
        connected.append((signal, handler))
        return handler

    yield _connect

    for sig, handler in connected:
        sig.disconnect(handler)


# ═══════════════════════════════════════════════════════════════════════════
# Signal dispatch tests
# ═══════════════════════════════════════════════════════════════════════════


class TestEventScheduledSignal:
    """event_scheduled signal fires on creation with status='scheduled'."""

    def test_signal_sent_on_create_scheduled(self, signal_spy) -> None:  # noqa: ANN001
        handler = signal_spy(event_scheduled)
        event = LaunchEventFactory(status="scheduled")
        handler.assert_called_once()
        call_kwargs = handler.call_args[1]
        assert call_kwargs["sender"] == LaunchEvent
        assert call_kwargs["instance"].pk == event.pk

    def test_signal_not_sent_for_non_scheduled(self, signal_spy) -> None:  # noqa: ANN001
        handler = signal_spy(event_scheduled)
        LaunchEventFactory(status="launched")
        handler.assert_not_called()


class TestEventStatusChangedSignal:
    """event_status_changed signal fires when status is modified."""

    def test_signal_sent_on_status_update(self, signal_spy) -> None:  # noqa: ANN001
        handler = signal_spy(event_status_changed)
        event = LaunchEventFactory(status="scheduled")
        event.status = "launched"
        event.save()
        handler.assert_called_once()

    def test_signal_includes_old_and_new_status(self, signal_spy) -> None:  # noqa: ANN001
        handler = signal_spy(event_status_changed)
        event = LaunchEventFactory(status="scheduled")
        event.status = "scrubbed"
        event.save()
        call_kwargs = handler.call_args[1]
        assert call_kwargs["old_status"] == "scheduled"
        assert call_kwargs["new_status"] == "scrubbed"

    def test_signal_not_sent_when_status_unchanged(self, signal_spy) -> None:  # noqa: ANN001
        handler = signal_spy(event_status_changed)
        event = LaunchEventFactory(status="scheduled")
        event.name = "Renamed"
        event.save()
        handler.assert_not_called()


# ═══════════════════════════════════════════════════════════════════════════
# Audit log receiver tests
# ═══════════════════════════════════════════════════════════════════════════


class TestAuditLogReceivers:
    """Receivers create AuditLog entries on signal dispatch."""

    def test_audit_log_created_on_schedule(self) -> None:
        event = LaunchEventFactory(status="scheduled")
        log = AuditLog.objects.filter(event=event, action="SCHEDULED").first()
        assert log is not None
        assert event.name in log.details

    def test_audit_log_created_on_status_change(self) -> None:
        event = LaunchEventFactory(status="scheduled")
        event.status = "launched"
        event.save()
        log = AuditLog.objects.filter(
            event=event, action="STATUS_CHANGED"
        ).first()
        assert log is not None
        assert "scheduled" in log.details
        assert "launched" in log.details
