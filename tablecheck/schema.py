"""Explicit column rules; no guessed types or silent coercion."""

import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .audit import SAMPLE_LIMIT
from .reader import InputError


def number(value):
    try:
        result = Decimal(str(value))
        if result.is_finite():
            return result
    except InvalidOperation:
        pass
    return None


def load_schema(path, headers):
    with Path(path).open("rb") as source:
        raw = source.read(65_537)
    if len(raw) > 65_536:
        raise InputError("Schema exceeds the 64 KiB limit.")
    try:
        schema = json.loads(raw.decode("utf-8-sig"))
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise InputError("Schema must be valid UTF-8 JSON.") from exc
    validate_schema(schema, headers)
    return schema


def validate_schema(schema, headers):
    if not isinstance(schema, dict) or set(schema) != {"columns"} or not isinstance(schema["columns"], dict):
        raise InputError('Schema must contain only a "columns" object.')
    for column, rule in schema["columns"].items():
        if column not in headers:
            raise InputError(f"Schema column {column!r} is absent from the CSV header.")
        if not isinstance(rule, dict) or set(rule) - {"required", "type", "min", "max", "allowed"}:
            raise InputError(f"Column {column!r}: invalid rule or unknown rule key.")
        if "required" in rule and not isinstance(rule["required"], bool):
            raise InputError("required must be true or false.")
        if "type" in rule and rule["type"] not in ("string", "number"):
            raise InputError("type must be string or number.")
        for bound in ("min", "max"):
            if bound in rule and (rule.get("type") != "number" or type(rule[bound]) not in (int, float)
                                  or number(rule[bound]) is None):
                raise InputError("min/max need type number and finite JSON numeric bounds.")
        if "min" in rule and "max" in rule and rule["min"] > rule["max"]:
            raise InputError("min cannot exceed max.")
        if "allowed" in rule and (not isinstance(rule["allowed"], list) or not rule["allowed"]
                                  or any(not isinstance(v, str) for v in rule["allowed"])):
            raise InputError("allowed must be a nonempty array of strings.")


def apply_schema(report, headers, rows, schema):
    validate_schema(schema, headers)
    for column, rule in schema["columns"].items():
        index = headers.index(column)
        for record, row in enumerate(rows, 2):
            value = row[index]
            codes = []
            if not value.strip():
                if rule.get("required"):
                    codes.append("required")
            else:
                if rule.get("type") == "number":
                    parsed = number(value)
                    if parsed is None:
                        codes.append("not_number")
                    elif (("min" in rule and parsed < number(rule["min"]))
                          or ("max" in rule and parsed > number(rule["max"]))):
                        codes.append("out_of_range")
                if "allowed" in rule and value not in rule["allowed"]:
                    codes.append("not_allowed")
            for code in codes:
                report["issue_count"] += 1
                if len(report["issues"]) < SAMPLE_LIMIT:
                    report["issues"].append({"code": code, "record": record, "column": column})
    report["issues_truncated"] = report["issue_count"] > len(report["issues"])
    return report
