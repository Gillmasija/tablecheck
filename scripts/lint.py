"""Dependency-free syntax and source hygiene checks (not a style linter)."""

import ast
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
paths = [p for folder in ("tablecheck", "tests", "scripts") for p in (root / folder).rglob("*.py")]
for path in paths:
    source = path.read_text(encoding="utf-8")
    try:
        ast.parse(source, filename=str(path), feature_version=(3, 10))
    except SyntaxError as exc:
        errors.append(str(exc))
    for line, text in enumerate(source.splitlines(), 1):
        if text.rstrip() != text or "\t" in text:
            errors.append(f"{path.relative_to(root)}:{line}: trailing whitespace or tab")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Lint passed: {len(paths)} Python files; 3.10 syntax and source hygiene.")
