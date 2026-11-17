"""Self-contained, script-free HTML reports. All source labels are escaped."""

from html import escape

STYLE = """
:root{font-family:system-ui,sans-serif;color:#17352f;background:#f5f7f3;line-height:1.6}
*{box-sizing:border-box}body{margin:0}header,main,footer{max-width:1080px;margin:auto;padding:24px}
header{display:flex;justify-content:space-between;gap:16px;align-items:center;border-bottom:1px solid #ccd8d0}
.brand{font-weight:800;letter-spacing:.03em}.mark{background:#17634f;color:white;border-radius:7px;padding:5px 9px;margin-right:8px}
nav{display:flex;gap:18px;flex-wrap:wrap}a{color:#17634f;text-underline-offset:4px}a:focus-visible,summary:focus-visible{outline:3px solid #ad4e16;outline-offset:4px}
h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1.15;letter-spacing:-.04em;margin:16px 0}h2{font-size:1.35rem;margin:0 0 16px}
.eyebrow{font-size:.75rem;font-weight:800;letter-spacing:.13em;color:#42685d;text-transform:uppercase}
.lede{max-width:640px;color:#486158}.badge{display:inline-block;background:#e8eee9;border:1px solid #bdcfc3;border-radius:20px;padding:4px 12px;font-size:.8rem}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:28px 0}
.metric,section{background:white;border:1px solid #d8e1da;border-radius:12px;padding:24px}.metric strong{display:block;font-size:2rem;line-height:1.3}.metric span{font-size:.85rem;color:#486158}
section{margin:20px 0;scroll-margin-top:20px}.section-head{display:flex;justify-content:space-between;gap:16px;align-items:center}.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.9rem}caption{text-align:left;color:#486158;margin-bottom:14px}th{text-align:left;background:#f1f5f0}th,td{padding:12px;border-bottom:1px solid #e1e7e2;overflow-wrap:anywhere}th[scope=row]{background:white;font-weight:600;max-width:320px}
progress{display:block;width:100%;max-width:130px;height:7px;accent-color:#ad4e16}summary{cursor:pointer;font-weight:600}details p,details ul{max-width:760px}.muted{color:#486158;font-size:.88rem}.notice{border-left:4px solid #ad4e16;padding:12px 16px;background:#fff5e9;border-radius:4px}
code{font-size:.86em;background:#edf2ed;padding:2px 5px;border-radius:4px}footer{font-size:.8rem;color:#486158}
@media(max-width:640px){header{align-items:flex-start;flex-direction:column}header,main,footer{padding:18px}.metrics{grid-template-columns:repeat(2,1fr);gap:10px}.metric,section{padding:16px}.section-head{align-items:flex-start;flex-direction:column}th,td{padding:8px}}
@media print{body{background:white;color:black}header,main,footer{max-width:none;padding:10px}nav{display:none}.metric,section{border-color:#aaa;box-shadow:none}tr,.metric{break-inside:avoid}.table-wrap{overflow:visible}a{color:black}}
"""

MESSAGES = {
    "missing": "Blank cell; check whether a value is expected.",
    "duplicate_row": "Exact repeat of an earlier record; confirm it is intentional.",
    "required": "A required column is blank.",
    "not_number": "Expected a finite number.",
    "out_of_range": "Number is outside the configured inclusive bounds.",
    "not_allowed": "Value does not exactly match an allowed category.",
}


def html_report(report):
    profiles = "".join(
        f'<tr><th scope="row">{escape(c["name"])}</th><td>{c["distinct"]}</td>'
        f'<td>{c["missing"]}</td><td>{c["missing_percent"]}%'
        f'<progress aria-label="Missing percent" max="100" value="{c["missing_percent"]}"></progress></td></tr>'
        for c in report["columns"])
    findings = "".join(
        f'<tr><td>{i["record"]}</td><td>{escape(i["column"]) if i["column"] is not None else "Whole record"}</td>'
        f'<td><code>{escape(i["code"])}</code><br>{MESSAGES[i["code"]]}</td></tr>'
        for i in report["issues"])
    status = "Needs review" if report["issue_count"] else "No findings"
    empty = '<p class="notice">Header only: no data records to assess. Add records and run again.</p>' if not report["rows"] else ""
    findings_section = (
        '<div class="table-wrap"><table><caption>Record numbers include the header. Multiline cells count as one record.</caption>'
        '<thead><tr><th scope="col">Record</th><th scope="col">Column</th><th scope="col">Finding / next step</th></tr></thead>'
        f'<tbody>{findings}</tbody></table></div>' if findings else
        '<p>No issues were found by the configured checks. This does not establish that the data is correct.</p>')
    metrics = "".join(f'<div class="metric"><strong>{value}</strong><span>{label}</span></div>' for label, value in (
        ("Data records", report["rows"]), ("Columns", len(report["columns"])),
        ("Findings", report["issue_count"]), ("Duplicate records", report["duplicate_rows"])))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Offline CSV quality audit: profiles, findings and next steps.">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'">
<title>TableCheck | Data quality report</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='9' fill='%2317634f'/%3E%3Cpath d='M10 20l7 7 14-15' fill='none' stroke='white' stroke-width='4'/%3E%3C/svg%3E">
<style>{STYLE}</style></head><body>
<header><div class="brand"><span class="mark" aria-hidden="true">✓</span>TABLECHECK</div>
<nav aria-label="Report sections"><a href="#overview">Overview</a><a href="#profiles">Columns</a><a href="#findings">Findings</a></nav></header>
<main id="overview"><p class="eyebrow">Know your data before the next step</p>
<h1>A clearer picture of your CSV.</h1><p class="lede">Review completeness, repeated records and explicit rule checks. Your source file stays unchanged; the decisions stay with you.</p>
<span class="badge">{status} · Offline report · v{report["report_version"]}</span>{empty}
<div class="metrics" aria-label="Audit summary">{metrics}</div>
<section id="profiles"><div class="section-head"><h2>Column health</h2><span class="muted">Blank after trimming = missing</span></div>
<div class="table-wrap"><table><caption>Distinct counts exclude blank cells and compare exact source text.</caption>
<thead><tr><th scope="col">Column</th><th scope="col">Distinct</th><th scope="col">Missing</th><th scope="col">Missing share</th></tr></thead>
<tbody>{profiles}</tbody></table></div></section>
<section id="findings"><div class="section-head"><h2>Review queue</h2><span class="badge">{len(report["issues"])} of {report["issue_count"]} findings shown</span></div>
<p class="muted">Samples are capped at 100; counts include all findings. One cell can trigger multiple checks. Cell values are omitted.</p>{findings_section}</section>
<section><h2>What to do next</h2><ol><li>Locate each flagged record in the original CSV.</li><li>Confirm the intended value or whether a repeated record is legitimate.</li><li>Save any corrections separately, then run TableCheck again.</li></ol>
<details><summary>How to read this report</summary><p>Missing cells and exact duplicate records are flagged without a schema. Optional schema rules add required, finite-number, inclusive range and exact allowed-category checks. Rules do not infer business meaning.</p>
<p>Duplicate records compare all raw cells; distinct values are also exact. Numeric checks permit surrounding whitespace and scientific notation. Allowed categories are case-sensitive and untrimmed.</p>
<p>Use your browser's Print command to save this report as PDF. Expand this explanation first if you want it included. Column headers remain visible, so review them before sharing.</p></details></section></main>
<footer>TableCheck · Generated locally · No external assets, scripts, analytics or network requests.</footer></body></html>'''
