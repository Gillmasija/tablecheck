# Verification — 2026-11-17

## Local checks

- Python 3.15.2 on Windows: `python -m unittest discover -v` — 14 tests passed.
- `python scripts/lint.py` — 17 Python files pass Python 3.10 syntax and source hygiene checks.
- `python scripts/build.py` — portable zipapp built; clean example exits 0 and findings example exits 1.
- `git diff --check` — passed.
- Synthetic schema journey: 8 records, 4 columns, 1 duplicate, 6 findings; JSON and HTML exports.
- Missing file, invalid CSV/UTF-8/schema, input limits, missing parent directory and overwrite refusal tested.
- Source preserved byte-for-byte when requested as output; HTML source labels escaped; JSON omits cell values.

## Browser QA

Edge on Windows, actual generated `docs/example-report.html`:

- Desktop: summary, labeled column table, six-location review queue and matching favicon rendered.
- Findings/Overview anchors navigate correctly.
- Methodology disclosure expands with Enter (native details.open verified true).
- 390px and 320px widths: no document overflow. Tables scroll inside their own region.
- At 320px, keyboard ArrowRight changed the column region scroll position.
- Fixed cramped mobile column headings after initial inspection; reloaded and rechecked.
- Viewport override reset. Desktop and mobile screenshots saved beside this file.
- Print stylesheet provided; physical print/PDF export was not tested.

The local preview server was only for QA; users open the generated HTML directly.
No hosted app URL is claimed. The initial sandbox preview could not be reached by
Edge; local-only preview outside the sandbox worked.

## Review scope

Reports intentionally omit input filenames, cell values and schema definitions.
Keep the source/schema for interpretation. Reports retain column names. Exact
repeated records can be legitimate; no automatic corrections are made.

GitHub CI results are reported in the PR after the final push. Do not infer CI
success from these local checks alone.
