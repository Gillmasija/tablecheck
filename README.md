# TableCheck

A local CSV quality auditor for analysts preparing a dataset for a dashboard or
model. Python 3.10+; no runtime dependencies, accounts or network services.

Setup check: `python -m tablecheck`.

## Planned verified milestones

1. Working Python package setup (`Setup done`).
2. Project brief and acceptance criteria; open draft PR before implementation.
3. Strict UTF-8 CSV ingestion and useful input errors.
4. Column profiles, missingness and duplicate-row detection.
5. Explicit JSON schema rules for required, numeric and allowed values.
6. CLI with readable summary and meaningful exit codes.
7. Machine-readable JSON report and safe output handling.
8. Accessible offline HTML report with matching favicon and print styles.
9. Synthetic fixtures and end-to-end/error-path regression coverage.
10. Automated lint, packaging and CI checks.
11. User guide, acceptance evidence and final review handoff.

Every milestone is checked and committed before the next begins. This is a
Python CLI with a generated report, not a hosted web application.
