"""Test suite for Week 9 — Repository Pattern & Protocol-Driven Design.

Run:  pytest test_starter.py -v

╔══════════════════════════════════════════════════════════════════╗
║  IMPORTANT: This file NEVER imports InMemoryRepository.         ║
║  All repository tests use the `repository` fixture from         ║
║  conftest.py.  In Week 11 you swap ONLY the fixture — these     ║
║  tests run against your Django implementation with zero edits.  ║
╚══════════════════════════════════════════════════════════════════╝

All 26 tests FAIL against the stubs.  Make them pass.
"""

from __future__ import annotations

import pytest

from starter import (
    EntityNotFoundError,
    EventService,
    LaunchEvent,
    Repository,
)

# ── helpers ────────────────────────────────────────────────────────────────


def _make_event(**overrides: str) -> LaunchEvent:
    """Return a LaunchEvent with sensible defaults, overridable by kwargs."""
    defaults = {
        "id": "evt-001",
        "name": "Falcon 9 Launch",
        "date": "2025-06-15",
        "location": "Cape Canaveral",
        "status": "scheduled",
    }
    defaults.update(overrides)
    return LaunchEvent(**defaults)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════
# Task 1 — LaunchEvent entity
# ═══════════════════════════════════════════════════════════════════════════


class TestLaunchEvent:
    """Domain entity identity and representation."""

    def test_create_event(self) -> None:
        evt = _make_event()
        assert evt.id == "evt-001"
        assert evt.name == "Falcon 9 Launch"
        assert evt.status == "scheduled"

    def test_equality_by_id(self) -> None:
        """Two events with the same id are equal, even if names differ."""
        a = _make_event(id="same-id", name="Alpha")
        b = _make_event(id="same-id", name="Beta")
        assert a == b

    def test_inequality_different_ids(self) -> None:
        a = _make_event(id="id-1")
        b = _make_event(id="id-2")
        assert a != b

    def test_repr_format(self) -> None:
        evt = _make_event(id="abc", name="Starship")
        assert repr(evt) == "LaunchEvent(id='abc', name='Starship')"


# ═══════════════════════════════════════════════════════════════════════════
# Task 2 — EntityNotFoundError
# ═══════════════════════════════════════════════════════════════════════════


class TestEntityNotFoundError:
    """Custom exception semantics."""

    def test_stores_entity_id(self) -> None:
        err = EntityNotFoundError("xyz-123")
        assert err.entity_id == "xyz-123"

    def test_str_message(self) -> None:
        err = EntityNotFoundError("xyz-123")
        assert str(err) == "Entity with id 'xyz-123' not found"


# ═══════════════════════════════════════════════════════════════════════════
# Tasks 3 & 4 — Repository contract tests
# (All tests use the `repository` fixture — NEVER a concrete class)
# ═══════════════════════════════════════════════════════════════════════════


class TestRepositoryAdd:
    """Adding entities to the repository."""

    def test_add_returns_entity(self, repository: Repository[LaunchEvent]) -> None:
        evt = _make_event()
        result = repository.add(evt)
        assert result == evt

    def test_add_duplicate_id_raises(self, repository: Repository[LaunchEvent]) -> None:
        evt = _make_event(id="dup")
        repository.add(evt)
        with pytest.raises(ValueError, match="already exists"):
            repository.add(_make_event(id="dup", name="Different"))


class TestRepositoryGet:
    """Retrieving entities by id."""

    def test_get_existing(self, repository: Repository[LaunchEvent]) -> None:
        evt = _make_event(id="get-me")
        repository.add(evt)
        found = repository.get("get-me")
        assert found.name == evt.name

    def test_get_missing_raises(self, repository: Repository[LaunchEvent]) -> None:
        with pytest.raises(EntityNotFoundError) as exc_info:
            repository.get("ghost")
        assert exc_info.value.entity_id == "ghost"


class TestRepositoryListAll:
    """Listing all entities."""

    def test_list_all_empty(self, repository: Repository[LaunchEvent]) -> None:
        assert repository.list_all() == []

    def test_list_all_returns_all(self, repository: Repository[LaunchEvent]) -> None:
        repository.add(_make_event(id="1", name="A"))
        repository.add(_make_event(id="2", name="B"))
        result = repository.list_all()
        assert len(result) == 2
        ids = {e.id for e in result}
        assert ids == {"1", "2"}


class TestRepositoryUpdate:
    """Updating existing entities."""

    def test_update_existing(self, repository: Repository[LaunchEvent]) -> None:
        repository.add(_make_event(id="u1", name="Original"))
        updated_evt = _make_event(id="u1", name="Updated")
        result = repository.update(updated_evt)
        assert result.name == "Updated"
        assert repository.get("u1").name == "Updated"

    def test_update_missing_raises(self, repository: Repository[LaunchEvent]) -> None:
        with pytest.raises(EntityNotFoundError):
            repository.update(_make_event(id="nope"))


class TestRepositoryDelete:
    """Deleting entities."""

    def test_delete_existing(self, repository: Repository[LaunchEvent]) -> None:
        repository.add(_make_event(id="del-me"))
        repository.delete("del-me")
        assert len(repository.list_all()) == 0

    def test_delete_missing_raises(self, repository: Repository[LaunchEvent]) -> None:
        with pytest.raises(EntityNotFoundError):
            repository.delete("ghost")

    def test_delete_then_get_raises(self, repository: Repository[LaunchEvent]) -> None:
        repository.add(_make_event(id="temp"))
        repository.delete("temp")
        with pytest.raises(EntityNotFoundError):
            repository.get("temp")


class TestRepositoryFilterBy:
    """Attribute-based filtering."""

    @pytest.fixture(autouse=True)
    def _seed_events(self, repository: Repository[LaunchEvent]) -> None:
        repository.add(_make_event(id="1", name="A", status="scheduled", location="KSC"))
        repository.add(_make_event(id="2", name="B", status="launched", location="KSC"))
        repository.add(_make_event(id="3", name="C", status="scheduled", location="Vandenberg"))
        repository.add(_make_event(id="4", name="D", status="scrubbed", location="Vandenberg"))

    def test_filter_by_status(self, repository: Repository[LaunchEvent]) -> None:
        result = repository.filter_by(status="scheduled")
        assert len(result) == 2
        assert all(e.status == "scheduled" for e in result)

    def test_filter_by_location(self, repository: Repository[LaunchEvent]) -> None:
        result = repository.filter_by(location="Vandenberg")
        assert len(result) == 2

    def test_filter_by_multiple_fields(self, repository: Repository[LaunchEvent]) -> None:
        result = repository.filter_by(status="scheduled", location="KSC")
        assert len(result) == 1
        assert result[0].name == "A"

    def test_filter_by_no_match(self, repository: Repository[LaunchEvent]) -> None:
        result = repository.filter_by(status="exploded")
        assert result == []


# ═══════════════════════════════════════════════════════════════════════════
# Task 5 — EventService (service layer via dependency injection)
# ═══════════════════════════════════════════════════════════════════════════


class TestEventService:
    """Service layer business logic."""

    @pytest.fixture()
    def service(self, repository: Repository[LaunchEvent]) -> EventService:
        return EventService(repo=repository)

    def test_schedule_creates_with_scheduled_status(
        self, service: EventService
    ) -> None:
        evt = service.schedule_event("Test Launch", "2025-08-01", "KSC")
        assert evt.status == "scheduled"
        assert evt.name == "Test Launch"
        assert len(evt.id) > 0  # uuid hex

    def test_schedule_assigns_unique_ids(self, service: EventService) -> None:
        a = service.schedule_event("A", "2025-01-01", "KSC")
        b = service.schedule_event("B", "2025-01-02", "KSC")
        assert a.id != b.id

    def test_cancel_sets_scrubbed(
        self, service: EventService, repository: Repository[LaunchEvent]
    ) -> None:
        evt = service.schedule_event("Cancel Me", "2025-09-01", "KSC")
        cancelled = service.cancel_event(evt.id)
        assert cancelled.status == "scrubbed"
        assert repository.get(evt.id).status == "scrubbed"

    def test_cancel_missing_raises(self, service: EventService) -> None:
        with pytest.raises(EntityNotFoundError):
            service.cancel_event("no-such-id")

    def test_get_upcoming_filters_correctly(
        self, service: EventService
    ) -> None:
        service.schedule_event("Past", "2025-01-01", "KSC")
        service.schedule_event("Future A", "2025-07-01", "KSC")
        service.schedule_event("Future B", "2025-08-01", "Vandenberg")

        # Cancel Future B
        upcoming_all = service.get_upcoming("2025-06-01")
        assert len(upcoming_all) == 2

        # Only events on or after 2025-07-15
        upcoming_late = service.get_upcoming("2025-07-15")
        assert len(upcoming_late) == 1
        assert upcoming_late[0].name == "Future B"
