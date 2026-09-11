# Week 13 — Django Signals, Middleware & Custom Auth Backend

## Objective

Extend the launch-events Django app with three foundational infrastructure
layers that every production SaaS needs:

1. **Custom signals** — decouple side-effects (audit logging) from business logic.
2. **Custom middleware** — inject cross-cutting concerns into the request/response cycle.
3. **Custom auth backend** — organisation-scoped, role-based permission checks.

By the end of this lab you'll understand how Django's internals (`Signal`,
`MiddlewareMixin`, `BaseBackend`) work, and you'll have the RBAC foundation
that Week 16 builds into a full permission system.

---

## 🔗 Connection to Month 3

| Month 3 Artefact | How It's Used Here |
|------------------|--------------------|
| `LaunchEvent` model (Week 11) | Signals fire when events are created/updated |
| `EventService` (Week 9 → 11) | Service calls trigger signals via model `save()` |
| Django project scaffold (Week 12) | Settings, URLs, middleware stack |
| Repository Protocol (Week 9) | Proves the pattern: tests don't care about infra |

---

## Tasks

### Task 1 — Custom Signals + Audit Logging

**File: `events/signals.py`** — define two custom signals:
- `event_scheduled` — sent when a `LaunchEvent` is created with `status="scheduled"`.
  Provides: `sender` (model class), `instance` (the event).
- `event_status_changed` — sent when a `LaunchEvent`'s `status` field changes.
  Provides: `sender`, `instance`, `old_status`, `new_status`.

**File: `events/receivers.py`** — connect receivers that create `AuditLog` entries:
- `log_event_scheduled(sender, instance, **kwargs)` → creates AuditLog with
  `action="SCHEDULED"`, `event=instance`, `details=f"Event '{instance.name}' scheduled"`.
- `log_status_change(sender, instance, old_status, new_status, **kwargs)` → creates
  AuditLog with `action="STATUS_CHANGED"`,
  `details=f"Status changed from '{old_status}' to '{new_status}'"`.

**File: `events/models.py`** — override `LaunchEvent.save()`:
- Before `super().save()`, fetch the old status from DB (if `self.pk` exists).
- After `super().save()`, send the appropriate signal(s).

**File: `events/apps.py`** — import receivers in `ready()` to connect them.

### Task 2 — Custom Middleware

**File: `events/middleware.py`** — implement two middleware classes:

| Class | Behaviour |
|-------|-----------|
| `RequestTimingMiddleware` | Measures wall-clock time of each request. Adds `X-Request-Duration-Ms` response header (float, milliseconds). |
| `OrganizationMiddleware` | Reads `X-Organization-Slug` request header. If present, looks up `Organization` by slug, sets `request.organization`. If header is absent, sets `request.organization = None`. If slug doesn't match any org, returns a **404 JSON response**: `{"error": "Organization not found"}`. |

### Task 3 — Custom Auth Backend + RBAC Models

**File: `accounts/models.py`** — define:
- `Organization` — `name` (CharField), `slug` (SlugField, unique).
- `Membership` — links `User` ↔ `Organization` with a `role` field.
  Roles: `viewer`, `member`, `admin`. Unique together on `(user, organization)`.

**File: `accounts/backends.py`** — implement `OrganizationBackend`:

| Method | Behaviour |
|--------|-----------|
| `authenticate(request, username, password, **kwargs)` | Standard username/password check. Return `None` for invalid credentials or inactive users. |
| `has_perm(user_obj, perm, obj=None)` | If `obj` is an `Organization`, look up the user's `Membership.role` in that org and check against `ROLE_PERMISSIONS`. Return `False` if no membership exists. |
| `get_user(user_id)` | Return `User` by pk, or `None`. |

**Permission matrix:**

| Permission | viewer | member | admin |
|-----------|--------|--------|-------|
| `events.view_event` | ✅ | ✅ | ✅ |
| `events.add_event` | ❌ | ✅ | ✅ |
| `events.change_event` | ❌ | ✅ | ✅ |
| `events.delete_event` | ❌ | ❌ | ✅ |
| `events.manage_members` | ❌ | ❌ | ✅ |

---

## File Layout

```
labs/week13_signals_middleware_auth/
├── README.md
├── manage.py
├── pyproject.toml
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── urls.py
├── events/                      ← LaunchEvent model provided (carry-forward)
│   ├── __init__.py
│   ├── apps.py                  ← STUB: connect signals in ready()
│   ├── models.py                ← PARTIAL: LaunchEvent provided, save() + AuditLog are stubs
│   ├── signals.py               ← STUB
│   ├── receivers.py             ← STUB
│   └── middleware.py            ← STUB
├── accounts/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                ← STUB: Organization, Membership
│   └── backends.py              ← STUB: OrganizationBackend
└── tests/
    ├── __init__.py
    ├── factories.py             ← provided: factory_boy factories
    ├── test_signals.py          ← 7 tests
    ├── test_middleware.py       ← 5 tests
    └── test_auth_backend.py     ← 9 tests
```

---

## How to Run

```bash
cd labs/week13_signals_middleware_auth

# Install dependencies (first time only)
pip install django pytest pytest-django factory-boy

# Run tests
pytest -v

# Lint
ruff check events/ accounts/

# Type-check
mypy events/ accounts/ --strict --ignore-missing-imports
```

---

## Pass Bar

```
22 passed in <Ns
```
