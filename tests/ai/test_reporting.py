from infra_ai.reporting.report import render_report


def test_render_report_with_findings() -> None:
    findings = [
        {
            "severity": "HIGH",
            "category": "SECURITY",
            "resource": "test.security_group.insecure",
            "title": "SSH exposed to the internet",
            "description": "Security group permits SSH access from 0.0.0.0/0.",
            "recommendation": (
                "Restrict SSH access to a trusted CIDR "
                "or use AWS Systems Manager."
            ),
        }
    ]

    report = render_report(1, findings)

    assert "Infrastructure Analysis" in report
    assert "Resources analyzed: 1" in report
    assert "Findings: 1" in report
    assert "[HIGH] SECURITY" in report
    assert "SSH exposed to the internet" in report
    assert "test.security_group.insecure" in report
    assert "0.0.0.0/0" in report
    assert "Recommendation:" in report
    assert "AWS Systems Manager" in report


def test_render_report_without_findings() -> None:
    report = render_report(38, [])

    assert "Resources analyzed: 38" in report
    assert "Findings: 0" in report
    assert "No infrastructure issues detected." in report
