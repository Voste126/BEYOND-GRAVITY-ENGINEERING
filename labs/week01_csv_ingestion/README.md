# Week 1 — CSV Ingestion Pipeline

## Objective

Build a typed, test-driven CSV ingestion pipeline for launch-event data.
You will parse raw CSV files, validate and type-convert each row, filter by
criteria, and produce summary statistics — all from pure Python with no
third-party CSV libraries (use only the `csv` module from the stdlib).

This is the data layer that every future week builds on.

---

## Learning Outcomes

- Read and parse CSV files safely using `csv.DictReader`.
- Validate data with explicit, informative error messages.
- Filter and aggregate collections using list comprehensions and `dict` operations.
- Handle edge cases: missing files, empty files, malformed rows, bad types.
- Write fully typed public APIs (PEP 484).

---

## CSV Schema

Each row in a launch-event CSV has these columns:

| Column       | Type   | Rules                                                        |
|-------------|--------|--------------------------------------------------------------|
| `event_name` | str    | Required, non-empty.                                         |
| `date`       | str    | Required, ISO-8601 format (`YYYY-MM-DD`).                    |
| `location`   | str    | Required, non-empty.                                         |
| `attendees`  | int    | Required, must be a positive integer (> 0).                  |
| `status`     | str    | Required, one of: `scheduled`, `launched`, `scrubbed`.       |

---

## Tasks

### Task 1 — `parse_csv(filepath)`
Read a CSV file and return a `list[dict[str, str]]` of raw string rows.
Raise `FileNotFoundError` for missing files. Raise `ValueError` for empty
files (header-only or truly empty).

### Task 2 — `validate_row(row)`
Accept a raw `dict[str, str]` row and return a validated `dict[str, Any]`
with `attendees` converted to `int`. Raise `ValueError` with a descriptive
message for any validation failure (missing field, bad date format, non-positive
attendees, invalid status).

### Task 3 — `filter_events(events, *, status, min_attendees)`
Filter a list of validated event dicts. Both keyword arguments are optional;
when `None`, that filter is skipped. Return a new list (do not mutate the input).

### Task 4 — `summarize_events(events)`
Return a summary dict with keys: `total_events`, `total_attendees`,
`avg_attendees` (float, rounded to 2 decimals), and `by_status`
(a dict mapping each status string to its count). Raise `ValueError`
if the input list is empty.

### Task 5 — `ingest_pipeline(filepath, *, status, min_attendees)`
Compose tasks 1-4: parse → validate every row → filter → summarize.
Collect per-row validation errors into a `errors: list[str]` key in the
returned dict alongside the summary keys. Valid rows continue through the
pipeline even if other rows fail validation.

---

## How to Run

```bash
# From the repo root:
cd labs/week01_csv_ingestion

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
