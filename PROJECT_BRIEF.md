# TableCheck project brief

## User and problem

Junior analysts and data educators need to assess a CSV before building charts
or training models. TableCheck surfaces missing cells, duplicate rows and
explicit rule violations while keeping source data on the user's machine.

## Scope and design

Dependency-free Python 3.10+ CLI, UTF-8 comma-separated CSV, opt-in JSON schema,
terminal summary, JSON output and a self-contained HTML report. No AI, automatic
data cleaning, inferred correctness, telemetry, server or deployment required.
Original synthetic course-enrolment fixtures only. Demonstrates Python data
processing, defensive validation, accessible report design and automated testing.

Keep source values unchanged. Missing means blank after trimming whitespace;
duplicate rows compare exact raw cells. Numeric values must be finite decimals.
Row numbers are CSV record numbers including the header (not physical lines for
multiline quoted fields). No raw values in reports by default.

## Acceptance checklist

- [x] Read UTF-8/BOM files with quoted commas/newlines, reject malformed rows.
- [x] Show row/column counts, missingness, distinct counts and duplicate records.
- [x] Validate required, number, min/max and allowed-value schema rules.
- [x] Report actionable record/column locations without exposing cell contents.
- [x] Produce readable terminal, versioned JSON and offline HTML reports.
- [x] HTML is responsive, keyboard usable, printable and safely escapes text.
- [x] Exit 0 for clean, 1 for findings, 2 for input/config/output errors.
- [x] Never modify input files; refuse overwrite of report files by default.
- [x] Clear errors for empty, invalid UTF-8, missing files and invalid schemas.
- [x] Synthetic demo, usage guide, automated tests, lint, build and CI pass.

## Milestones and limitations

Follow the eleven separately verified milestones in README.md. Draft PR must
exist before parser implementation. Up to 10 MiB input, 100,000 records and 200
columns, with bounded issue samples; small datasets only. No XLSX, streaming
large files, locale-specific numbers, automatic type inference or cloud sync.
Exact duplicates may be legitimate: findings are review prompts, not corrections.
