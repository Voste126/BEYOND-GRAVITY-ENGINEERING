# Week 9 — Repository Pattern & Protocol-Driven Design

## Objective

Build a **generic Repository pattern** backed by `typing.Protocol`, then
implement it with a pure-Python in-memory store.  The critical design
constraint: your test suite is written against the `Repository` *interface*,
not the `InMemoryRepository` class.  In Week 11 you will build a second,
Django-ORM-backed implementation that passes **this exact same test file**
with only a one-line fixture swap in `conftest.py`.

This is the pattern real-world SaaS platforms use to stay testable: business
logic depends on abstractions, never on database details.

---

## 🔗 Connection to Month 1

| Month 1 Concept | How It Returns Here |
|-----------------|---------------------|
| Typed functions (Week 1) | Every method has PEP 484 signatures |
| `__eq__`, `__repr__` (Week 2) | `LaunchEvent` uses identity-by-ID equality |
| Protocols (Week 3) | `Repository[T]` is a `typing.Protocol` |
| Generics (Week 4 LRU) | Repository is generic over its entity type |

---

## 🔮 Week 11 Bridge

Your `conftest.py` currently wires the `repository` fixture to
`InMemoryRepository`.  In Week 11 you will:

1. Create a `DjangoRepository` that talks to the ORM.
2. Replace **only** `conftest.py` to yield `DjangoRepository`.
3. Run `pytest test_starter.py -v` — **all tests pass, zero changes to the
   test file.**

If your tests import concrete classes or call implementation-specific
methods, they won't be reusable.  Design accordingly.

---

## Tasks

### Task 1 — `LaunchEvent` (domain entity)

A `@dataclass` with fields: `id: str`, `name: str`, `date: str` (ISO-8601),
`location: str`, `status: str` (one of `scheduled`, `launched`, `scrubbed`).

- `__eq__` compares by `id` only (two events with the same `id` are equal
  regardless of other fields — this is DDD entity identity).
- `__hash__` is consistent with `__eq__` (hash on `id`).
- `__repr__` returns `"LaunchEvent(id='...', name='...')"` (id and name only).

### Task 2 — `EntityNotFoundError`

A custom exception inheriting `Exception`.  Constructor takes `entity_id: str`
and stores it as an attribute.  `str(error)` must return
`"Entity with id '<id>' not found"`.

### Task 3 — `Repository[T]` (protocol)

A `typing.Protocol` (runtime-checkable) defining the contract:

| Method | Signature | Raises |
|--------|-----------|--------|
| `add` | `(entity: T) -> T` | `ValueError` if `id` already exists |
| `get` | `(entity_id: str) -> T` | `EntityNotFoundError` |
| `list_all` | `() -> list[T]` | — |
| `update` | `(entity: T) -> T` | `EntityNotFoundError` |
| `delete` | `(entity_id: str) -> None` | `EntityNotFoundError` |
| `filter_by` | `(**kwargs: Any) -> list[T]` | — |

### Task 4 — `InMemoryRepository[T]`

A concrete implementation of the `Repository` protocol backed by a plain
`dict[str, T]`.  `filter_by` matches entity attributes against `**kwargs`
using `getattr`.

### Task 5 — `EventService` (service layer)

Depends on `Repository[LaunchEvent]` via constructor injection.

| Method | Behaviour |
|--------|-----------|
| `schedule_event(name, date, location) -> LaunchEvent` | Creates with `status="scheduled"` and a `uuid4` hex id. Adds via repo. |
| `cancel_event(event_id: str) -> LaunchEvent` | Sets `status="scrubbed"`, calls `repo.update()`. Raises `EntityNotFoundError` if missing. |
| `get_upcoming(min_date: str) -> list[LaunchEvent]` | Returns events with `status="scheduled"` **and** `date >= min_date` (string comparison is fine for ISO dates). |

---

## File Layout

```
labs/week09_repository_pattern/
├── README.md            ← you are here
├── starter.py           ← stubs (Tasks 1-5)
├── conftest.py          ← pytest fixture: provides `repository`
└── test_starter.py      ← contract tests (DO NOT reference InMemoryRepository)
```

---

## How to Run

```bash
cd labs/week09_repository_pattern

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
26 passed in <1s
```
