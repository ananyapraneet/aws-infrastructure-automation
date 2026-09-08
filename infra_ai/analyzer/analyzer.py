from typing import Any

from infra_ai.analyzer.iam import find_missing_ec2_iam_policies
from infra_ai.analyzer.network import find_missing_private_endpoints
from infra_ai.analyzer.security import (
    find_public_application_exposure,
    find_public_ssh_exposure,
)


def analyze_resources(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings = []

    findings.extend(find_public_ssh_exposure(resources))
    findings.extend(find_public_application_exposure(resources))
    findings.extend(find_missing_ec2_iam_policies(resources))
    findings.extend(find_missing_private_endpoints(resources))

    return findings
