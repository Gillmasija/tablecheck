import json
import tempfile
import unittest
from pathlib import Path

from tablecheck.audit import audit
from tablecheck.html_report import html_report
from tablecheck.reader import InputError
from tablecheck.reports import json_report, write_report


class ReportTests(unittest.TestCase):
    def test_html_escapes_source_labels_and_explains_empty_state(self):
        content = html_report(audit(['<script>alert("x")</script>'], [[""]]))
        self.assertNotIn('<script>', content)
        self.assertIn('&lt;script&gt;', content)
        self.assertIn('rel="icon"', content)
        self.assertIn('Header only', html_report(audit(["id"], [])))
        self.assertIn('No issues were found', html_report(audit(["id"], [["A"]])))

    def test_json_contract_omits_cell_values(self):
        report = audit(["name"], [["PRIVATE_VALUE"], ["PRIVATE_VALUE"]])
        serialized = json_report(report)
        self.assertNotIn("PRIVATE_VALUE", serialized)
        self.assertEqual(json.loads(serialized)["report_version"], 1)
        self.assertEqual(json.loads(serialized)["issues"][0]["record"], 3)

    def test_exclusive_output_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.json"
            write_report(path, "original")
            with self.assertRaises(InputError):
                write_report(path, "replacement")
            self.assertEqual(path.read_text(), "original")
