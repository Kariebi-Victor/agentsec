
import json

import agentsec.reporter as reporter


def test_report_generation(tmp_path, monkeypatch):
    monkeypatch.setattr(reporter, "REPORT_DIR", tmp_path)

    result = {
        "assessment": "Two authorization findings confirmed.",
        "tool_results": [
            {
                "check": "idor",
                "endpoint": "/api/users/2",
                "status_code": 200,
                "potential_vulnerability": True,
                "evidence": "Unauthorized access to another user record",
            },
            {
                "check": "broken_function_level_authorization",
                "endpoint": "/api/admin/stats",
                "status_code": 200,
                "potential_vulnerability": True,
                "evidence": "Regular user accessed admin endpoint",
            },
        ],
    }

    json_path, html_path = reporter.generate_reports(result)

    assert json_path.exists()
    assert html_path.exists()

    report = json.loads(json_path.read_text(encoding="utf-8"))

    assert report["findings_count"] == 2
    assert len(report["findings"]) == 2
    assert report["findings"][0]["severity"] == "High"

    html = html_path.read_text(encoding="utf-8")

    assert "AgentSec Security Assessment" in html
    assert "Broken Object Level Authorization" in html


def test_html_escaping(tmp_path, monkeypatch):
    monkeypatch.setattr(reporter, "REPORT_DIR", tmp_path)

    result = {
        "assessment": "<script>alert('test')</script>",
        "tool_results": [],
    }

    _, html_path = reporter.generate_reports(result)

    html = html_path.read_text(encoding="utf-8")

    assert "&lt;script&gt;" in html
    assert "<script>" not in html
