import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-m", "tablecheck", *map(str, args)],
                              capture_output=True, text=True)

    def test_exit_codes_and_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.csv"
            path.write_text("id,score\nA,0\n", encoding="utf-8")
            self.assertEqual(self.run_cli(path).returncode, 0)
            path.write_text("id,score\nA,\n", encoding="utf-8")
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Record 2", result.stdout)
            result = self.run_cli(Path(folder) / "missing.csv")
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_help_and_version(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)
        self.assertIn("0.1.0", self.run_cli("--version").stdout)
