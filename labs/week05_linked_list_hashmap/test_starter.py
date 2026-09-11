"""Test suite for Week 5 — Linked Lists & Hash Maps from Scratch.

Run:  pytest test_starter.py -v
All 36 tests FAIL against the stubs.  Make them pass.
"""

from __future__ import annotations

import pytest

from starter import HashMap, Node, SinglyLinkedList

# ═══════════════════════════════════════════════════════════════════════════
# Task 1 — Node
# ═══════════════════════════════════════════════════════════════════════════


class TestNode:
    """Tests for the Node data container."""

    def test_node_stores_value(self) -> None:
        node = Node(42)
        assert node.value == 42

    def test_node_next_defaults_to_none(self) -> None:
        node = Node("hello")
        assert node.next is None

    def test_node_links_to_another_node(self) -> None:
        second = Node(2)
        first = Node(1, next_node=second)
        assert first.next is second
        assert first.next.value == 2


# ═══════════════════════════════════════════════════════════════════════════
# Task 2 — SinglyLinkedList
# ═══════════════════════════════════════════════════════════════════════════


class TestSinglyLinkedListBasics:
    """Core operations: prepend, append, len."""

    def test_new_list_is_empty(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        assert len(ll) == 0

    def test_prepend_increases_len(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.prepend(10)
        ll.prepend(20)
        assert len(ll) == 2

    def test_prepend_inserts_at_head(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.prepend(1)
        ll.prepend(2)
        ll.prepend(3)
        assert list(ll) == [3, 2, 1]

    def test_append_inserts_at_tail(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert list(ll) == [1, 2, 3]

    def test_mixed_prepend_append(self) -> None:
        ll: SinglyLinkedList[str] = SinglyLinkedList()
        ll.append("b")
        ll.prepend("a")
        ll.append("c")
        assert list(ll) == ["a", "b", "c"]


class TestSinglyLinkedListDelete:
    """Deletion edge cases."""

    def test_delete_head(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.delete(1)
        assert list(ll) == [2, 3]
        assert len(ll) == 2

    def test_delete_middle(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.delete(2)
        assert list(ll) == [1, 3]

    def test_delete_tail(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.delete(3)
        assert list(ll) == [1, 2]
        assert len(ll) == 2

    def test_delete_only_element(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(99)
        ll.delete(99)
        assert len(ll) == 0
        assert list(ll) == []

    def test_delete_not_found_raises(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(1)
        with pytest.raises(ValueError, match="42 not found in list"):
            ll.delete(42)

    def test_delete_from_empty_raises(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        with pytest.raises(ValueError, match="1 not found in list"):
            ll.delete(1)


class TestSinglyLinkedListFind:
    """Lookup via find()."""

    def test_find_existing_value(self) -> None:
        ll: SinglyLinkedList[str] = SinglyLinkedList()
        ll.append("a")
        ll.append("b")
        ll.append("c")
        assert ll.find("b") == 1

    def test_find_head(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(10)
        ll.append(20)
        assert ll.find(10) == 0

    def test_find_not_found_raises(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(1)
        with pytest.raises(ValueError, match="99 not found in list"):
            ll.find(99)


class TestSinglyLinkedListReverse:
    """In-place reversal."""

    def test_reverse_multiple(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        for v in [1, 2, 3, 4]:
            ll.append(v)
        ll.reverse()
        assert list(ll) == [4, 3, 2, 1]

    def test_reverse_single(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(42)
        ll.reverse()
        assert list(ll) == [42]

    def test_reverse_empty_is_noop(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.reverse()  # should not raise
        assert len(ll) == 0


class TestSinglyLinkedListDunders:
    """__contains__ and __repr__."""

    def test_contains_true(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(5)
        ll.append(10)
        assert 10 in ll

    def test_contains_false(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(5)
        assert 99 not in ll

    def test_repr_with_elements(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert repr(ll) == "1 -> 2 -> 3 -> None"

    def test_repr_empty(self) -> None:
        ll: SinglyLinkedList[int] = SinglyLinkedList()
        assert repr(ll) == "None"


# ═══════════════════════════════════════════════════════════════════════════
# Task 3 — HashMap
# ═══════════════════════════════════════════════════════════════════════════


class TestHashMapCore:
    """put, get, delete basics."""

    def test_put_and_get(self) -> None:
        hm: HashMap[str, int] = HashMap()
        hm.put("alpha", 1)
        hm.put("beta", 2)
        assert hm.get("alpha") == 1
        assert hm.get("beta") == 2

    def test_put_overwrites_existing_key(self) -> None:
        hm: HashMap[str, str] = HashMap()
        hm.put("key", "old")
        hm.put("key", "new")
        assert hm.get("key") == "new"
        assert len(hm) == 1  # no duplicate entry

    def test_get_missing_raises_key_error(self) -> None:
        hm: HashMap[str, int] = HashMap()
        with pytest.raises(KeyError):
            hm.get("missing")

    def test_delete_existing_key(self) -> None:
        hm: HashMap[str, int] = HashMap()
        hm.put("x", 10)
        hm.delete("x")
        assert "x" not in hm
        assert len(hm) == 0

    def test_delete_missing_raises_key_error(self) -> None:
        hm: HashMap[str, int] = HashMap()
        with pytest.raises(KeyError):
            hm.delete("ghost")


class TestHashMapDunders:
    """__contains__ and __len__."""

    def test_contains_true(self) -> None:
        hm: HashMap[int, str] = HashMap()
        hm.put(42, "answer")
        assert 42 in hm

    def test_contains_false(self) -> None:
        hm: HashMap[int, str] = HashMap()
        assert 42 not in hm

    def test_len_tracks_insertions_and_deletions(self) -> None:
        hm: HashMap[str, int] = HashMap()
        assert len(hm) == 0
        hm.put("a", 1)
        hm.put("b", 2)
        assert len(hm) == 2
        hm.delete("a")
        assert len(hm) == 1


class TestHashMapViews:
    """keys() and values()."""

    def test_keys_returns_all_keys(self) -> None:
        hm: HashMap[str, int] = HashMap()
        hm.put("x", 1)
        hm.put("y", 2)
        hm.put("z", 3)
        assert sorted(hm.keys()) == ["x", "y", "z"]

    def test_values_returns_all_values(self) -> None:
        hm: HashMap[str, int] = HashMap()
        hm.put("x", 10)
        hm.put("y", 20)
        assert sorted(hm.values()) == [10, 20]


class TestHashMapResize:
    """Auto-resize behaviour."""

    def test_resize_preserves_entries(self) -> None:
        """Insert enough keys to force at least one resize (capacity=4,
        threshold at 3 entries), then verify all entries survive."""
        hm: HashMap[int, str] = HashMap(capacity=4)
        entries = {i: f"val_{i}" for i in range(10)}
        for k, v in entries.items():
            hm.put(k, v)
        assert len(hm) == 10
        for k, v in entries.items():
            assert hm.get(k) == v

    def test_many_insertions_stress(self) -> None:
        """Stress test: 200 unique keys, all retrievable after resizes."""
        hm: HashMap[int, int] = HashMap()
        for i in range(200):
            hm.put(i, i * i)
        assert len(hm) == 200
        for i in range(200):
            assert hm.get(i) == i * i
