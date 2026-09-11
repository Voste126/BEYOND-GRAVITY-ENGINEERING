"""Week 5 — Linked Lists & Hash Maps from Scratch (starter stubs).

Implement every class below so that `pytest test_starter.py -v` goes green.
Only stdlib imports are allowed (you should not need any).
"""

from __future__ import annotations

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


# ---------------------------------------------------------------------------
# Task 1 — Node
# ---------------------------------------------------------------------------


class Node(Generic[T]):
    """A single node in a singly linked list.

    Attributes:
        value: The data stored in this node.
        next: Reference to the next node, or ``None`` if this is the tail.
    """

    __slots__ = ("value", "next")

    def __init__(self, value: T, next_node: Node[T] | None = None) -> None:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 2 — SinglyLinkedList
# ---------------------------------------------------------------------------


class SinglyLinkedList(Generic[T]):
    """A generic singly linked list with O(1) prepend and append.

    Maintains ``_head``, ``_tail``, and ``_size`` internally.
    """

    def __init__(self) -> None:
        """Initialise an empty list."""
        raise NotImplementedError

    # -- insertion ----------------------------------------------------------

    def prepend(self, value: T) -> None:
        """Insert *value* at the head of the list.  O(1)."""
        raise NotImplementedError

    def append(self, value: T) -> None:
        """Insert *value* at the tail of the list.  O(1)."""
        raise NotImplementedError

    # -- deletion -----------------------------------------------------------

    def delete(self, value: T) -> None:
        """Remove the first node whose value equals *value*.

        Raises:
            ValueError: ``"{value} not found in list"``
        """
        raise NotImplementedError

    # -- lookup -------------------------------------------------------------

    def find(self, value: T) -> int:
        """Return the 0-based index of the first node matching *value*.

        Raises:
            ValueError: ``"{value} not found in list"``
        """
        raise NotImplementedError

    # -- mutation -----------------------------------------------------------

    def reverse(self) -> None:
        """Reverse the list **in place**.  O(n) time, O(1) extra space."""
        raise NotImplementedError

    # -- dunder protocols ---------------------------------------------------

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError

    def __contains__(self, value: object) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        """Format as ``'1 -> 2 -> 3 -> None'``.  Empty list: ``'None'``."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 3 — HashMap
# ---------------------------------------------------------------------------


class HashMap(Generic[K, V]):
    """A separate-chaining hash map.

    Internal storage is a Python ``list`` of buckets.  Each bucket is a
    Python ``list`` of ``(key, value)`` tuples.  The map auto-resizes
    (doubles capacity) when the load factor exceeds 0.75.
    """

    _LOAD_FACTOR_THRESHOLD: float = 0.75

    def __init__(self, capacity: int = 8) -> None:
        """Create a hash map with *capacity* initial buckets."""
        raise NotImplementedError

    # -- core operations ----------------------------------------------------

    def put(self, key: K, value: V) -> None:
        """Insert *key*/*value* or update *value* if *key* already exists.

        Triggers ``_resize()`` **after** insertion when load factor > 0.75.
        """
        raise NotImplementedError

    def get(self, key: K) -> V:
        """Return the value associated with *key*.

        Raises:
            KeyError: if *key* is not present.
        """
        raise NotImplementedError

    def delete(self, key: K) -> None:
        """Remove *key* and its value from the map.

        Raises:
            KeyError: if *key* is not present.
        """
        raise NotImplementedError

    # -- views --------------------------------------------------------------

    def keys(self) -> list[K]:
        """Return all keys (order not guaranteed)."""
        raise NotImplementedError

    def values(self) -> list[V]:
        """Return all values (order not guaranteed)."""
        raise NotImplementedError

    # -- internal -----------------------------------------------------------

    def _resize(self) -> None:
        """Double the capacity and rehash all existing entries."""
        raise NotImplementedError

    # -- dunder protocols ---------------------------------------------------

    def __contains__(self, key: object) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
