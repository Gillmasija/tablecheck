"""Deterministic profiles with bounded, value-free issue locations."""

SAMPLE_LIMIT = 100


def audit(headers, rows):
    report = {"report_version": 1, "rows": len(rows), "columns": [],
              "duplicate_rows": 0, "issue_count": 0, "issues": []}

    def issue(code, record, column=None):
        report["issue_count"] += 1
        if len(report["issues"]) < SAMPLE_LIMIT:
            report["issues"].append({"code": code, "record": record, "column": column})

    seen = set()
    for record, row in enumerate(rows, 2):
        key = tuple(row)
        if key in seen:
            report["duplicate_rows"] += 1
            issue("duplicate_row", record)
        seen.add(key)
    for index, name in enumerate(headers):
        missing = 0
        distinct = set()
        for record, row in enumerate(rows, 2):
            value = row[index]
            if not value.strip():
                missing += 1
                issue("missing", record, name)
            else:
                distinct.add(value)
        report["columns"].append({"name": name, "missing": missing,
                                  "distinct": len(distinct),
                                  "missing_percent": round(missing / len(rows) * 100, 2) if rows else 0})
    report["issues_truncated"] = report["issue_count"] > len(report["issues"])
    return report
