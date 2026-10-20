
import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path


REPORT_DIR = Path("reports")


FINDING_METADATA = {
    "idor": {
        "title": "Broken Object Level Authorization (BOLA/IDOR)",
        "severity": "High",
        "owasp": "API1:2023",
        "remediation": (
            "Enforce object-level authorization on every request. "
            "Verify that the authenticated user owns the requested "
            "resource or has explicit permission to access it."
        ),
    },
    "broken_function_level_authorization": {
        "title": "Broken Function Level Authorization",
        "severity": "High",
        "owasp": "API5:2023",
        "remediation": (
            "Enforce server-side role and permission checks "
            "on administrative endpoints."
        ),
    },
}


def generate_reports(result):
    REPORT_DIR.mkdir(exist_ok=True)

    findings = []

    for item in result["tool_results"]:
        if not item["potential_vulnerability"]:
            continue

        metadata = FINDING_METADATA[item["check"]]

        findings.append({
            "title": metadata["title"],
            "severity": metadata["severity"],
            "owasp": metadata["owasp"],
            "endpoint": item["endpoint"],
            "status_code": item["status_code"],
            "evidence": item["evidence"],
            "remediation": metadata["remediation"],
        })

    report = {
        "tool": "AgentSec",
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": "http://127.0.0.1:8000",
        "findings_count": len(findings),
        "findings": findings,
        "llm_assessment": result["assessment"],
    }

    json_path = REPORT_DIR / "agentsec-report.json"
    html_path = REPORT_DIR / "agentsec-report.html"

    json_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    rows = ""

    for finding in findings:
        rows += f"""
        <tr>
            <td>{escape(finding['title'])}</td>
            <td><span class="severity">{escape(finding['severity'])}</span></td>
            <td>{escape(finding['endpoint'])}</td>
            <td>{escape(finding['evidence'])}</td>
            <td>{escape(finding['remediation'])}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AgentSec Security Assessment</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                padding: 40px;
                line-height: 1.6;
            }}
            h1 {{ color: #38bdf8; }}
            .summary {{
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: #1e293b;
            }}
            th, td {{
                padding: 15px;
                border: 1px solid #334155;
                text-align: left;
                vertical-align: top;
            }}
            th {{ background: #334155; }}
            .severity {{
                color: #f87171;
                font-weight: bold;
            }}
            .assessment {{
                white-space: pre-wrap;
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <h1>AgentSec Security Assessment</h1>

        <div class="summary">
            <p><strong>Target:</strong> Local Vulnerable API</p>
            <p><strong>Findings:</strong> {len(findings)}</p>
            <p><strong>Generated:</strong> {escape(report['generated_at'])}</p>
        </div>

        <h2>Security Findings</h2>

        <table>
            <thead>
                <tr>
                    <th>Finding</th>
                    <th>Severity</th>
                    <th>Endpoint</th>
                    <th>Evidence</th>
                    <th>Remediation</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <h2>AI Assessment</h2>
        <div class="assessment">{escape(result['assessment'])}</div>
    </body>
    </html>
    """

    html_path.write_text(html, encoding="utf-8")

    return json_path, html_path
