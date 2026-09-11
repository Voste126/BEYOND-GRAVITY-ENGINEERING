"""Test suite for Week 1 — CSV Ingestion Pipeline.

Run:  pytest test_starter.py -v
All 26 tests FAIL against the stubs.  Make them pass.
"""

from __future__ import annotations

import csv
import textwrap
from pathlib import Path
from typing import Any

import pytest

from starter import (
    VALID_STATUSES,
    filter_events,
    ingest_pipeline,
    parse_csv,
    summarize_events,
    validate_row,
)

# ── helpers ────────────────────────────────────────────────────────────────


def _write_csv(tmp_path: Path, filename: str, text: str) -> str:
    """Write dedented *text* to a CSV file and return its path as a string."""
    p = tmp_path / filename
    p.write_text(textwrap.dedent(text).strip() + "\n")
    return str(p)


def _good_row(**overrides: str) -> dict[str, str]:
    """Return a valid raw row dict, with optional field overrides."""
    base: dict[str, str] = {
        "event_name": "Falcon 9 Launch",
        "date": "2025-03-15",
        "location": "Cape Canaveral",
        "attendees": "500",
        "status": "scheduled",
    }
    base.update(overrides)
    return base


def _validated_row(**overrides: Any) -> dict[str, Any]:
    """Return an already-validated event dict (attendees is int)."""
    base: dict[str, Any] = {
        "event_name": "Falcon 9 Launch",
        "date": "2025-03-15",
        "location": "Cape Canaveral",
        "attendees": 500,
        "status": "scheduled",
    }
    base.update(overrides)
    return base


# ═══════════════════════════════════════════════════════════════════════════
# Task 1 — parse_csv
# ═══════════════════════════════════════════════════════════════════════════


class TestParseCSV:
    """Tests for parse_csv()."""

    def test_parse_valid_csv(self, tmp_path: Path) -> None:
        path = _write_csv(
            tmp_path,
            "events.csv",
            """\
            event_name,date,location,attendees,status
            Falcon 9 Launch,2025-03-15,Cape Canaveral,500,scheduled
            Starship Test,2025-04-01,Boca Chica,1200,launched
            """,
        )
        rows = parse_csv(path)
        assert len(rows) == 2
        assert rows[0]["event_name"] == "Falcon 9 Launch"
        assert rows[1]["attendees"] == "1200"  # still a string at this stage

    def test_parse_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            parse_csv("/nonexistent/path/events.csv")

    def test_parse_empty_file(self, tmp_path: Path) -> None:
        path = _write_csv(tmp_path, "empty.csv", "")
        with pytest.raises(ValueError):
            parse_csv(path)

    def test_parse_header_only(self, tmp_path: Path) -> None:
        path = _write_csv(
            tmp_path,
            "header_only.csv",
            "event_name,date,location,attendees,status",
        )
        with pytest.raises(ValueError):
            parse_csv(path)


# ═══════════════════════════════════════════════════════════════════════════
# Task 2 — validate_row
# ═══════════════════════════════════════════════════════════════════════════


class TestValidateRow:
    """Tests for validate_row()."""

    def test_valid_row_converts_attendees(self) -> None:
        result = validate_row(_good_row())
        assert result["attendees"] == 500
        assert isinstance(result["attendees"], int)

    def test_valid_row_preserves_strings(self) -> None:
        result = validate_row(_good_row())
        assert result["event_name"] == "Falcon 9 Launch"
        assert result["status"] == "scheduled"

    def test_missing_event_name(self) -> None:
        with pytest.raises(ValueError, match="event_name"):
            validate_row(_good_row(event_name=""))

    def test_missing_date(self) -> None:
        with pytest.raises(ValueError, match="date"):
            validate_row(_good_row(date=""))

    def test_invalid_date_format(self) -> None:
        with pytest.raises(ValueError, match="date"):
            validate_row(_good_row(date="15-03-2025"))

    def test_impossible_calendar_date(self) -> None:
        with pytest.raises(ValueError, match="date"):
            validate_row(_good_row(date="2025-02-30"))

    def test_attendees_not_a_number(self) -> None:
        with pytest.raises(ValueError, match="attendees"):
            validate_row(_good_row(attendees="abc"))

    def test_attendees_zero(self) -> None:
        with pytest.raises(ValueError, match="attendees"):
            validate_row(_good_row(attendees="0"))

    def test_attendees_negative(self) -> None:
        with pytest.raises(ValueError, match="attendees"):
            validate_row(_good_row(attendees="-5"))

    def test_invalid_status(self) -> None:
        with pytest.raises(ValueError, match="status"):
            validate_row(_good_row(status="cancelled"))


# ═══════════════════════════════════════════════════════════════════════════
# Task 3 — filter_events
# ═══════════════════════════════════════════════════════════════════════════


class TestFilterEvents:
    """Tests for filter_events()."""

    @pytest.fixture()
    def sample_events(self) -> list[dict[str, Any]]:
        return [
            _validated_row(event_name="A", status="scheduled", attendees=100),
            _validated_row(event_name="B", status="launched", attendees=500),
            _validated_row(event_name="C", status="scrubbed", attendees=50),
            _validated_row(event_name="D", status="scheduled", attendees=800),
        ]

    def test_no_filters_returns_all(
        self, sample_events: list[dict[str, Any]]
    ) -> None:
        result = filter_events(sample_events)
        assert len(result) == 4

    def test_filter_by_status(
        self, sample_events: list[dict[str, Any]]
    ) -> None:
        result = filter_events(sample_events, status="scheduled")
        assert all(e["status"] == "scheduled" for e in result)
        assert len(result) == 2

    def test_filter_by_min_attendees(
        self, sample_events: list[dict[str, Any]]
    ) -> None:
        result = filter_events(sample_events, min_attendees=200)
        assert all(e["attendees"] >= 200 for e in result)
        assert len(result) == 2

    def test_combined_filters(
        self, sample_events: list[dict[str, Any]]
    ) -> None:
        result = filter_events(
            sample_events, status="scheduled", min_attendees=200
        )
        assert len(result) == 1
        assert result[0]["event_name"] == "D"

    def test_does_not_mutate_input(
        self, sample_events: list[dict[str, Any]]
    ) -> None:
        original_len = len(sample_events)
        filter_events(sample_events, status="launched")
        assert len(sample_events) == original_len


# ═══════════════════════════════════════════════════════════════════════════
# Task 4 — summarize_events
# ═══════════════════════════════════════════════════════════════════════════


class TestSummarizeEvents:
    """Tests for summarize_events()."""

    def test_summary_counts(self) -> None:
        events = [
            _validated_row(attendees=100, status="scheduled"),
            _validated_row(attendees=200, status="launched"),
            _validated_row(attendees=300, status="scheduled"),
        ]
        result = summarize_events(events)
        assert result["total_events"] == 3
        assert result["total_attendees"] == 600
        assert result["avg_attendees"] == 200.0
        assert result["by_status"] == {"scheduled": 2, "launched": 1}

    def test_avg_attendees_rounded(self) -> None:
        events = [
            _validated_row(attendees=10),
            _validated_row(attendees=20),
            _validated_row(attendees=33),
        ]
        result = summarize_events(events)
        assert result["avg_attendees"] == 21.0

    def test_empty_list_raises(self) -> None:
        with pytest.raises(ValueError, match="No events to summarize"):
            summarize_events([])


# ═══════════════════════════════════════════════════════════════════════════
# Task 5 — ingest_pipeline
# ═══════════════════════════════════════════════════════════════════════════


class TestIngestPipeline:
    """Tests for ingest_pipeline()."""

    def test_full_pipeline_happy_path(self, tmp_path: Path) -> None:
        path = _write_csv(
            tmp_path,
            "good.csv",
            """\
            event_name,date,location,attendees,status
            Alpha,2025-06-01,KSC,300,scheduled
            Beta,2025-07-04,Vandenberg,150,launched
            """,
        )
        result = ingest_pipeline(path)
        assert result["total_events"] == 2
        assert result["errors"] == []

    def test_pipeline_skips_bad_rows(self, tmp_path: Path) -> None:
        path = _write_csv(
            tmp_path,
            "mixed.csv",
            """\
            event_name,date,location,attendees,status
            Good,2025-01-01,KSC,100,scheduled
            Bad,not-a-date,KSC,100,scheduled
            Also Good,2025-02-02,Vandenberg,200,launched
            """,
        )
        result = ingest_pipeline(path)
        assert result["total_events"] == 2
        assert len(result["errors"]) == 1
        assert "date" in result["errors"][0].lower()

    def test_pipeline_all_rows_invalid(self, tmp_path: Path) -> None:
        path = _write_csv(
            tmp_path,
            "all_bad.csv",
            """\
            event_name,date,location,attendees,status
            ,2025-01-01,KSC,100,scheduled
            Bad,2025-13-01,KSC,100,scheduled
            """,
        )
        result = ingest_pipeline(path)
        assert result["total_events"] == 0
        assert result["total_attendees"] == 0
        assert result["avg_attendees"] == 0.0
        assert result["by_status"] == {}
        assert len(result["errors"]) == 2

    def test_pipeline_propagates_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            ingest_pipeline("/no/such/file.csv")
