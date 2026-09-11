"""Week 9 — Repository Pattern & Protocol-Driven Design (starter stubs).

Implement every class below so that `pytest test_starter.py -v` goes green.
Only stdlib imports are allowed (uuid, dataclasses, typing).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable
import uuid


# ---------------------------------------------------------------------------
# Task 1 — LaunchEvent (domain entity)
# ---------------------------------------------------------------------------


@dataclass
class LaunchEvent:
    """A launch-event domain entity.

    Attributes:
        id: Unique identifier (UUID hex string).
        name: Human-readable event name.
        date: ISO-8601 date string (``YYYY-MM-DD``).
        location: Launch site name.
        status: One of ``scheduled``, ``launched``, ``scrubbed``.

    Equality and hashing are based on ``id`` alone (entity identity).

    ``__repr__`` returns ``"LaunchEvent(id='<id>', name='<name>')"``
    — only ``id`` and ``name``, not all fields.
    """

    id: str
    name: str
    date: str
    location: str
    status: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LaunchEvent):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"LaunchEvent(id={self.id!r}, name={self.name!r})"


# ---------------------------------------------------------------------------
# Task 2 — EntityNotFoundError & Domain Exceptions
# ---------------------------------------------------------------------------


class EntityNotFoundError(Exception):
    """Raised when a repository lookup fails.

    Attributes:
        entity_id: The ID that was not found.

    ``str(error)`` must return ``"Entity with id '<entity_id>' not found"``.
    """

    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
        super().__init__(f"Entity with id '{entity_id}' not found")

    def __str__(self) -> str:
        return f"Entity with id '{self.entity_id}' not found"


class DuplicateEntityError(ValueError):
    """Domain exception raised when attempting to add an entity with an existing id.

    Inherits from ValueError for backwards compatibility with repository test suites.
    """
    pass


# ---------------------------------------------------------------------------
# Task 3 — Repository protocol
# ---------------------------------------------------------------------------

T = TypeVar("T")


@runtime_checkable
class Repository(Protocol[T]):
    """Generic repository contract.

    Any class that implements these methods satisfies the protocol —
    no inheritance required.  This is what makes Week 11's Django swap
    possible.
    """

    def add(self, entity: T) -> T:
        """Persist *entity*.  Raise ``ValueError`` if its ``id`` already exists."""
        ...

    def get(self, entity_id: str) -> T:
        """Return the entity with *entity_id*.  Raise ``EntityNotFoundError`` if missing."""
        ...

    def list_all(self) -> list[T]:
        """Return all entities (order not guaranteed)."""
        ...

    def update(self, entity: T) -> T:
        """Replace the stored entity matching ``entity.id``.  Raise ``EntityNotFoundError`` if missing."""
        ...

    def delete(self, entity_id: str) -> None:
        """Remove entity with *entity_id*.  Raise ``EntityNotFoundError`` if missing."""
        ...

    def filter_by(self, **kwargs: Any) -> list[T]:
        """Return entities whose attributes match all *kwargs*."""
        ...


# ---------------------------------------------------------------------------
# Task 4 — InMemoryRepository
# ---------------------------------------------------------------------------


class InMemoryRepository(Generic[T]):
    """A dict-backed implementation of the :class:`Repository` protocol.

    Internal storage: ``dict[str, T]`` keyed by ``entity.id``.

    ``filter_by`` uses ``getattr(entity, key) == value`` for each kwarg.
    """

    def __init__(self) -> None:
        self._storage: dict[str, T] = {}

    def add(self, entity: T) -> T:
        """Persist *entity*.

        Raises:
            ValueError: with message ``"Entity with id '<id>' already exists"``
                if the id is already stored.
        """
        entity_id = getattr(entity, "id")
        if entity_id in self._storage:
            raise DuplicateEntityError(f"Entity with id '{entity_id}' already exists")
        self._storage[entity_id] = entity
        return entity

    def get(self, entity_id: str) -> T:
        """Retrieve by id.

        Raises:
            EntityNotFoundError: if *entity_id* is not stored.
        """
        if entity_id not in self._storage:
            raise EntityNotFoundError(entity_id)
        return self._storage[entity_id]

    def list_all(self) -> list[T]:
        """Return all stored entities as a list."""
        return list(self._storage.values())

    def update(self, entity: T) -> T:
        """Replace the stored entity whose id matches ``entity.id``.

        Raises:
            EntityNotFoundError: if the id is not stored.
        """
        entity_id = getattr(entity, "id")
        if entity_id not in self._storage:
            raise EntityNotFoundError(entity_id)
        self._storage[entity_id] = entity
        return entity

    def delete(self, entity_id: str) -> None:
        """Remove the entity with *entity_id*.

        Raises:
            EntityNotFoundError: if *entity_id* is not stored.
        """
        if entity_id not in self._storage:
            raise EntityNotFoundError(entity_id)
        del self._storage[entity_id]

    def filter_by(self, **kwargs: Any) -> list[T]:
        """Return entities matching all *kwargs* via ``getattr``."""
        return [
            entity
            for entity in self._storage.values()
            if all(getattr(entity, key, None) == val for key, val in kwargs.items())
        ]


# ---------------------------------------------------------------------------
# Task 5 — EventService (service layer)
# ---------------------------------------------------------------------------


class EventService:
    """Business logic layer — depends on a ``Repository[LaunchEvent]``.

    The repository is injected via the constructor (dependency injection).
    This class never imports or references ``InMemoryRepository`` directly.
    """

    def __init__(self, repo: Repository[LaunchEvent]) -> None:
        """Store the injected repository."""
        self._repo = repo

    def schedule_event(
        self, name: str, date: str, location: str
    ) -> LaunchEvent:
        """Create a new event with ``status='scheduled'`` and a uuid4 hex id.

        The event is added to the repository and returned.
        """
        event = LaunchEvent(
            id=uuid.uuid4().hex,
            name=name,
            date=date,
            location=location,
            status="scheduled",
        )
        return self._repo.add(event)

    def cancel_event(self, event_id: str) -> LaunchEvent:
        """Set an existing event's status to ``'scrubbed'`` and persist.

        Raises:
            EntityNotFoundError: if no event with *event_id* exists.
        """
        event = self._repo.get(event_id)
        event.status = "scrubbed"
        return self._repo.update(event)

    def get_upcoming(self, min_date: str) -> list[LaunchEvent]:
        """Return scheduled events on or after *min_date*.

        Filters by ``status='scheduled'`` AND ``date >= min_date``
        (lexicographic comparison is correct for ISO-8601 date strings).
        """
        scheduled = self._repo.filter_by(status="scheduled")
        return [e for e in scheduled if e.date >= min_date]
