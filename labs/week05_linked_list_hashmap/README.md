# Week 5 — Linked Lists & Hash Maps from Scratch

## Objective

Build a generic `SinglyLinkedList[T]` and a chaining-based `HashMap[K, V]`
from scratch — no stdlib collections beyond what Python gives you for free
(`list` literals for the backing array of buckets only). This lab proves you
understand how the data structures behind Python's `list` and `dict` actually
work under the hood.

---

## ⏱ Time Box: 60 minutes

Aim to finish the linked list in ≤ 20 min and spend the remaining 40 on the
hash map. If you blow the budget, note where you stalled — that's your
weak spot.

---

## 🎯 Big-O Targets

| Operation | SinglyLinkedList | HashMap (amortized) |
|-----------|-----------------|---------------------|
| `prepend` | O(1) | — |
| `append`  | O(1)* | — |
| `delete`  | O(n) | — |
| `find`    | O(n) | — |
| `reverse` | O(n) time, O(1) space | — |
| `put`     | — | O(1) amortized |
| `get`     | — | O(1) amortized |
| `delete`  | — | O(1) amortized |

\* O(1) append requires maintaining a `_tail` pointer.

---

## Tasks

### Task 1 — `Node[T]`
A simple container: `.value: T` and `.next: Node[T] | None`.

### Task 2 — `SinglyLinkedList[T]`
Implement a fully typed, generic singly linked list with:

- `prepend(value)` — insert at head, O(1).
- `append(value)` — insert at tail, O(1) using a tail pointer.
- `delete(value)` — remove the **first** occurrence. Raise `ValueError`
  with message `"{value} not found in list"` if absent.
- `find(value) -> int` — return 0-based index of first occurrence. Raise
  `ValueError` with message `"{value} not found in list"` if absent.
- `reverse()` — reverse **in place**, O(n) time, O(1) extra space.
- `__len__` — return count of nodes.
- `__iter__` — yield node values head → tail.
- `__contains__` — membership test.
- `__repr__` — format as `"1 -> 2 -> 3 -> None"` (empty list: `"None"`).

### Task 3 — `HashMap[K, V]`
Implement a separate-chaining hash map with:

- `__init__(capacity=8)` — start with the given number of buckets.
- `put(key, value)` — insert or **update** existing key. Trigger
  `_resize()` when load factor exceeds **0.75**.
- `get(key) -> V` — raise `KeyError(key)` if missing.
- `delete(key)` — raise `KeyError(key)` if missing.
- `__contains__(key)` — `True` if key exists.
- `__len__` — number of stored key-value pairs.
- `keys() -> list[K]` — all keys (order not guaranteed).
- `values() -> list[V]` — all values (order not guaranteed).
- `_resize()` — double capacity and rehash all entries.

---

## How to Run

```bash
cd labs/week05_linked_list_hashmap

# Run tests (they WILL fail until you implement starter.py)
pytest test_starter.py -v

# Lint
ruff check starter.py

# Type-check
mypy starter.py --strict

# Coverage
pytest test_starter.py --cov=starter --cov-report=term-missing
```

---

## Pass Bar

```
36 passed in <1s
```
