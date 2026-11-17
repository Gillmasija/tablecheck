import unittest

from tablecheck.audit import audit
from tablecheck.reader import InputError
from tablecheck.schema import apply_schema, validate_schema


class SchemaTests(unittest.TestCase):
    def test_numeric_required_and_allowed_rules(self):
        rows = [["0"], ["100.01"], ["NaN"], ["Infinity"], [" "], ["-1"], ["1e1"]]
        report = apply_schema(audit(["score"], rows), ["score"], rows,
                              {"columns": {"score": {"type": "number", "min": 0, "max": 100, "required": True}}})
        codes = [item["code"] for item in report["issues"]]
        self.assertEqual(codes.count("not_number"), 2)
        self.assertEqual(codes.count("out_of_range"), 2)
        self.assertEqual(codes.count("required"), 1)
        rows = [["yes"], [" yes"], [""]]
        report = apply_schema(audit(["x"], rows), ["x"], rows, {"columns": {"x": {"allowed": ["yes"]}}})
        self.assertEqual(report["issue_count"], 2)

    def test_invalid_schema_fails_instead_of_ignoring(self):
        bad = [[], {}, {"columns": []}, {"columns": {"absent": {}}}]
        for rule in ({"require": True}, {"required": "yes"}, {"min": 0}, {"type": "date"},
                     {"allowed": []}, {"allowed": [1]}, {"type": "number", "min": True},
                     {"type": "number", "max": float("inf")}, {"type": "number", "min": 2, "max": 1}):
            bad.append({"columns": {"x": rule}})
        for schema in bad:
            with self.subTest(schema=schema), self.assertRaises(InputError):
                validate_schema(schema, ["x"])
