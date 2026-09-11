"""Pytest fixtures for Week 9.

The ``repository`` fixture yields a fresh repository instance for each test.

┌──────────────────────────────────────────────────────────────────┐
│  WEEK 11 BRIDGE: swap the body of the `repository` fixture to   │
│  return your DjangoRepository instead.  NO test file changes.   │
└──────────────────────────────────────────────────────────────────┘
"""

from __future__ import annotations

import pytest

from starter import InMemoryRepository, LaunchEvent


@pytest.fixture()
def repository() -> InMemoryRepository[LaunchEvent]:
    """Provide a clean repository for each test."""
    return InMemoryRepository[LaunchEvent]()
