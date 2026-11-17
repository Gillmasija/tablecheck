import unittest

from tablecheck.audit import audit


class AuditTests(unittest.TestCase):
    def test_profiles_and_exact_duplicates(self):
        report = audit(["id", "score"], [["A", "0"], ["A", "0"], [" A", " "], ["B", ""]])
        self.assertEqual(report["duplicate_rows"], 1)
        self.assertEqual(report["issue_count"], 3)
        self.assertEqual(report["columns"][0]["distinct"], 3)
        self.assertEqual(report["columns"][1]["missing_percent"], 50)
        self.assertEqual(report["issues"][0]["record"], 3)

    def test_empty_dataset_and_bounded_samples(self):
        self.assertEqual(audit(["id"], [])["issue_count"], 0)
        report = audit(["id"], [[""]] * 200)
        self.assertEqual(report["issue_count"], 399)
        self.assertEqual(len(report["issues"]), 100)
        self.assertTrue(report["issues_truncated"])
