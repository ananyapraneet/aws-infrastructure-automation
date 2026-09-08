from typing import Any


def find_public_ssh_exposure(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings = []

    for resource in resources:
        if resource.get("type") != "aws_security_group":
            continue

        for rule in resource.get("values", {}).get("ingress", []):
            if (
                rule.get("protocol") == "tcp"
                and rule.get("from_port") <= 22 <= rule.get("to_port")
                and "0.0.0.0/0" in rule.get("cidr_blocks", [])
            ):
                findings.append(
                    {
                        "severity": "HIGH",
                        "category": "SECURITY",
                        "resource": resource.get("address"),
                        "title": "SSH exposed to the internet",
                        "description": (
                            "Security group permits SSH access from 0.0.0.0/0."
                        ),
                        "recommendation": (
                            "Restrict SSH access to a trusted CIDR or use "
                            "a managed access mechanism such as AWS Systems Manager."
                        ),
                    }
                )

    return findings

def find_public_application_exposure(
    resources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings = []

    for resource in resources:
        if resource.get("type") != "aws_security_group":
            continue

        for rule in resource.get("values", {}).get("ingress", []):
            if (
                rule.get("protocol") == "tcp"
                and rule.get("from_port") <= 8000 <= rule.get("to_port")
                and "0.0.0.0/0" in rule.get("cidr_blocks", [])
            ):
                findings.append(
                    {
                        "severity": "HIGH",
                        "category": "SECURITY",
                        "resource": resource.get("address"),
                        "title": "Application port exposed to the internet",
                        "description": (
                            "Security group permits direct access to the "
                            "application port from 0.0.0.0/0."
                        ),
                        "recommendation": (
                            "Restrict application traffic to the load balancer "
                            "security group or another trusted source."
                        ),
                    }
                )

    return findings
