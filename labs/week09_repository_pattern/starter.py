"""Week 9 — Repository Pattern & Protocol-Driven Design (starter stubs).

Implement every class below so that `pytest test_starter.py -v` goes green.
Only stdlib imports are allowed (uuid, dataclasses, typing).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable


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
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 2 — EntityNotFoundError
# ---------------------------------------------------------------------------


class EntityNotFoundError(Exception):
    """Raised when a repository lookup fails.

    Attributes:
        entity_id: The ID that was not found.

    ``str(error)`` must return ``"Entity with id '<entity_id>' not found"``.
    """

    def __init__(self, entity_id: str) -> None:
        raise NotImplementedError


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
        raise NotImplementedError

    def add(self, entity: T) -> T:
        """Persist *entity*.

        Raises:
            ValueError: with message ``"Entity with id '<id>' already exists"``
                if the id is already stored.
        """
        raise NotImplementedError

    def get(self, entity_id: str) -> T:
        """Retrieve by id.

        Raises:
            EntityNotFoundError: if *entity_id* is not stored.
        """
        raise NotImplementedError

    def list_all(self) -> list[T]:
        """Return all stored entities as a list."""
        raise NotImplementedError

    def update(self, entity: T) -> T:
        """Replace the stored entity whose id matches ``entity.id``.

        Raises:
            EntityNotFoundError: if the id is not stored.
        """
        raise NotImplementedError

    def delete(self, entity_id: str) -> None:
        """Remove the entity with *entity_id*.

        Raises:
            EntityNotFoundError: if *entity_id* is not stored.
        """
        raise NotImplementedError

    def filter_by(self, **kwargs: Any) -> list[T]:
        """Return entities matching all *kwargs* via ``getattr``."""
        raise NotImplementedError


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
        raise NotImplementedError

    def schedule_event(
        self, name: str, date: str, location: str
    ) -> LaunchEvent:
        """Create a new event with ``status='scheduled'`` and a uuid4 hex id.

        The event is added to the repository and returned.
        """
        raise NotImplementedError

    def cancel_event(self, event_id: str) -> LaunchEvent:
        """Set an existing event's status to ``'scrubbed'`` and persist.

        Raises:
            EntityNotFoundError: if no event with *event_id* exists.
        """
        raise NotImplementedError

    def get_upcoming(self, min_date: str) -> list[LaunchEvent]:
        """Return scheduled events on or after *min_date*.

        Filters by ``status='scheduled'`` AND ``date >= min_date``
        (lexicographic comparison is correct for ISO-8601 date strings).
        """
        raise NotImplementedError
