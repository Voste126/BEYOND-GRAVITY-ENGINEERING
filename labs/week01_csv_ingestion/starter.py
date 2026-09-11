"""Week 1 — CSV Ingestion Pipeline (starter stubs).

Implement every function below so that `pytest test_starter.py -v` goes green.
Do NOT add third-party dependencies; only the stdlib `csv` and `datetime` modules
are needed.
"""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Task 1
# ---------------------------------------------------------------------------

def parse_csv(filepath: str) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as a list of dicts.

    Each dict maps column-header → cell-value (both strings).

    Raises:
        FileNotFoundError: if *filepath* does not exist.
        ValueError: if the file is empty or contains only a header row.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 2
# ---------------------------------------------------------------------------

VALID_STATUSES: set[str] = {"scheduled", "launched", "scrubbed"}


def validate_row(row: dict[str, str]) -> dict[str, Any]:
    """Validate and type-convert a single raw CSV row.

    Returns a **new** dict with the same keys, where ``attendees`` is
    converted to ``int`` and all other values remain strings.

    Validation rules:
    - ``event_name``, ``date``, ``location``, ``status`` must be
      non-empty strings.
    - ``date`` must match ISO-8601 (``YYYY-MM-DD``) **and** be a real
      calendar date (e.g. ``2024-02-30`` is invalid).
    - ``attendees`` must convert to a positive ``int`` (> 0).
    - ``status`` must be one of :data:`VALID_STATUSES`.

    Raises:
        ValueError: with a human-readable message describing the first
            validation failure encountered.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 3
# ---------------------------------------------------------------------------

def filter_events(
    events: list[dict[str, Any]],
    *,
    status: str | None = None,
    min_attendees: int | None = None,
) -> list[dict[str, Any]]:
    """Return a filtered copy of *events*.

    Parameters:
        events: list of validated event dicts.
        status: if given, keep only events whose ``status`` equals this value.
        min_attendees: if given, keep only events with ``attendees >= min_attendees``.

    Both filters are optional; passing neither returns a shallow copy of the
    original list.  Passing both applies them with AND logic.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 4
# ---------------------------------------------------------------------------

def summarize_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Produce summary statistics for a list of validated events.

    Returns a dict with keys:
        - ``total_events``  (int)
        - ``total_attendees``  (int)
        - ``avg_attendees``  (float, rounded to 2 decimal places)
        - ``by_status``  (dict[str, int] — status → count)

    Raises:
        ValueError: with message ``"No events to summarize"`` when
            *events* is empty.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 5
# ---------------------------------------------------------------------------

def ingest_pipeline(
    filepath: str,
    *,
    status: str | None = None,
    min_attendees: int | None = None,
) -> dict[str, Any]:
    """End-to-end ingestion: parse → validate → filter → summarize.

    Rows that fail validation are **skipped** (not re-raised).  Their error
    messages are collected into an ``errors`` key (``list[str]``) in the
    returned dict, alongside the summary keys from :func:`summarize_events`.

    If **all** rows fail validation the function still returns a dict, but
    the summary values should be:
        ``total_events=0, total_attendees=0, avg_attendees=0.0,
          by_status={}, errors=[...]``

    Raises:
        FileNotFoundError: propagated from :func:`parse_csv`.
        ValueError: propagated from :func:`parse_csv` (empty file).
    """
    raise NotImplementedError
