"""Build a portable zipapp using only the standard library."""

import shutil
import subprocess
import sys
import tempfile
import zipapp
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output = root / "dist" / "tablecheck.pyz"
output.parent.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as folder:
    stage = Path(folder)
    shutil.copytree(root / "tablecheck", stage / "tablecheck", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    zipapp.create_archive(stage, output, main="tablecheck.cli:main", compressed=True)
    # zipapp's generated entry point discards return codes. Use our explicit one.
    (stage / "__main__.py").write_text("from tablecheck.cli import main\nraise SystemExit(main())\n", encoding="utf-8")
    zipapp.create_archive(stage, output, compressed=True)
    for fixture, expected in (("clean.csv", 0), ("enrolments.csv", 1)):
        result = subprocess.run([sys.executable, str(output), str(root / "examples" / fixture),
                                 "--schema", str(root / "examples" / "rules.json")], capture_output=True, text=True)
        if result.returncode != expected:
            raise SystemExit(f"Packaged journey failed: {result.stdout} {result.stderr}")
print("Build passed: dist/tablecheck.pyz; packaged clean and findings exit codes verified.")
