import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tablecheck.reader import InputError, read_csv
from tablecheck.schema import load_schema
from tests import test_cli


class JourneyTests(unittest.TestCase):
    run_cli = test_cli.CliTests.run_cli

    def test_synthetic_journey_and_source_protection(self):
        source = Path("examples/enrolments.csv")
        original = source.read_bytes()
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "report.json"
            args = (source, "--schema", "examples/rules.json", "--output", output)
            self.assertEqual(self.run_cli(*args).returncode, 1)
            report = json.loads(output.read_text())
            self.assertEqual((report["rows"], report["duplicate_rows"], report["issue_count"]), (8, 1, 6))
            self.assertEqual(self.run_cli(*args).returncode, 2)
            result = self.run_cli(source, "--output", source)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_bytes(), original)
            html = Path(folder) / "report.html"
            self.assertEqual(self.run_cli(source, "--format", "html", "--output", html).returncode, 1)
            self.assertIn("Column health", html.read_text(encoding="utf-8"))
        self.assertEqual(self.run_cli("examples/clean.csv", "--schema", "examples/rules.json").returncode, 0)

    def test_limits_and_config_errors(self):
        with patch("tablecheck.reader.MAX_BYTES", 5), self.assertRaises(InputError):
            read_csv("examples/clean.csv")
        with patch("tablecheck.reader.MAX_ROWS", 1), self.assertRaises(InputError):
            read_csv("examples/clean.csv")
        with patch("tablecheck.reader.MAX_COLUMNS", 2), self.assertRaises(InputError):
            read_csv("examples/clean.csv")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "schema.json"
            for content in ('{', '{"columns":{"x":{},"x":{}}}', 'a' * 65_537):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(InputError):
                    load_schema(path, ["x"])
            result = self.run_cli("examples/clean.csv", "--output", Path(folder) / "missing" / "file")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)
