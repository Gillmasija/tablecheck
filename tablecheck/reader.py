"""Strict, bounded CSV loading. Source cells are never rewritten."""

import csv
import io
from pathlib import Path

MAX_BYTES = 10 * 1024 * 1024
MAX_ROWS = 100_000
MAX_COLUMNS = 200


class InputError(ValueError):
    """An actionable input or configuration error."""


def read_csv(path):
    """Return (headers, rows), preserving original cells and record order."""
    with Path(path).open("rb") as source:
        raw = source.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise InputError("CSV exceeds the 10 MiB limit.")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputError("CSV must use UTF-8 encoding.") from exc
    if "\x00" in text:
        raise InputError("CSV contains NUL bytes; use a text CSV export.")
    try:
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        headers = next(reader, None)
        if not headers:
            raise InputError("CSV is empty or has no header.")
        if len(headers) > MAX_COLUMNS:
            raise InputError("CSV exceeds the 200-column limit.")
        if any(not name.strip() for name in headers):
            raise InputError("Every column needs a nonblank header.")
        if len({name.strip() for name in headers}) != len(headers):
            raise InputError("Column headers must be unique after trimming.")
        rows = []
        for record, row in enumerate(reader, 2):
            if len(rows) >= MAX_ROWS:
                raise InputError("CSV exceeds the 100,000-record limit.")
            if len(row) != len(headers):
                raise InputError(f"Record {record}: expected {len(headers)} cells, got {len(row)}.")
            rows.append(row)
        return headers, rows
    except csv.Error as exc:
        raise InputError("Malformed CSV quoting or field exceeds parser limit (128 KiB).") from exc
