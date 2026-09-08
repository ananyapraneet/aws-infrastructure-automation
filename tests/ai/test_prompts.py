from infra_ai.ai.prompts import build_analysis_prompt


def test_build_analysis_prompt_contains_findings():
    findings = [
        {
            "severity": "HIGH",
            "category": "SECURITY",
            "resource": "test.security_group.insecure",
            "title": "SSH exposed to the internet",
            "description": (
                "Security group permits SSH access from 0.0.0.0/0."
            ),
            "recommendation": (
                "Restrict SSH access to a trusted CIDR."
            ),
        }
    ]

    prompt = build_analysis_prompt(findings)

    assert "SSH exposed to the internet" in prompt
    assert "0.0.0.0/0" in prompt
    assert "Restrict SSH access to a trusted CIDR." in prompt
    assert "Do not invent infrastructure resources" in prompt
    assert "Do not suggest executing changes automatically" in prompt
    assert "Do not provide commands that modify infrastructure" in prompt
