"""Report serialization and exclusive output creation."""

import json
from pathlib import Path

from .reader import InputError


def json_report(report):
    return json.dumps(report, indent=2, ensure_ascii=True) + "\n"


def write_report(path, content):
    """Never overwrite existing files, including source data or symlinks."""
    try:
        with Path(path).open("x", encoding="utf-8", newline="\n") as target:
            target.write(content)
    except FileExistsError as exc:
        raise InputError("Report path already exists. Choose a new filename; nothing was overwritten.") from exc
