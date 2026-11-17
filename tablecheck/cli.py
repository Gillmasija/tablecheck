"""CLI orchestration and stable exit status contract."""

import argparse
import sys

from . import __version__
from .audit import audit
from .reader import InputError, read_csv
from .schema import apply_schema, load_schema


def summary(report):
    lines = ["TABLECHECK / CSV quality audit",
             f"{report['rows']} records | {len(report['columns'])} columns | "
             f"{report['issue_count']} findings | {report['duplicate_rows']} duplicate records"]
    if not report["rows"]:
        lines.append("No data records: header only. Add records before drawing conclusions.")
    for column in report["columns"]:
        lines.append(f"  {column['name']!r}: {column['missing']} missing "
                     f"({column['missing_percent']}%), {column['distinct']} distinct nonblank values")
    for issue in report["issues"][:10]:
        lines.append(f"  Record {issue['record']} / {issue['column']!r}: {issue['code']}")
    if report["issue_count"] > 10:
        lines.append("Terminal shows the first 10 findings; exported reports include up to 100.")
    lines.append("Review findings; source data has not been changed.")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit a local UTF-8 CSV without uploading data.")
    parser.add_argument("--version", action="version", version=f"TableCheck {__version__}")
    parser.add_argument("csv", help="CSV input (comma-separated, header required)")
    parser.add_argument("--schema", help="Optional JSON column rules")
    args = parser.parse_args(argv)
    try:
        headers, rows = read_csv(args.csv)
        report = audit(headers, rows)
        if args.schema:
            apply_schema(report, headers, rows, load_schema(args.schema, headers))
        print(summary(report))
        return 1 if report["issue_count"] else 0
    except (InputError, OSError) as exc:
        print(f"TableCheck error: {exc}", file=sys.stderr)
        return 2
