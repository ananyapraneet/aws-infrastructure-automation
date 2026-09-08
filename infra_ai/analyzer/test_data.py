from typing import Any


def get_controlled_findings() -> list[dict[str, Any]]:
    """Return intentionally insecure findings for AI integration testing."""

    return [
        {
            "severity": "HIGH",
            "category": "SECURITY",
            "resource": "test.security_group.insecure",
            "title": "SSH exposed to the internet",
            "description": (
                "Security group permits SSH access from 0.0.0.0/0."
            ),
            "recommendation": (
                "Restrict SSH access to a trusted CIDR or use "
                "AWS Systems Manager."
            ),
        }
    ]
