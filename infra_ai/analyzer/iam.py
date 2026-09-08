from typing import Any


REQUIRED_EC2_POLICIES = {
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
}


def find_missing_ec2_iam_policies(
    resources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings = []

    has_ec2_instance = any(
        resource.get("type") == "aws_instance"
        for resource in resources
    )

    if not has_ec2_instance:
        return []

    attached_policies = {
        resource.get("values", {}).get("policy_arn")
        for resource in resources
        if resource.get("type") == "aws_iam_role_policy_attachment"
    }

    missing_policies = REQUIRED_EC2_POLICIES - attached_policies

    if missing_policies:
        findings.append(
            {
                "severity": "HIGH",
                "category": "IAM",
                "resource": "aws_iam_role.ec2",
                "title": "Required EC2 IAM policies are missing",
                "description": (
                    "The EC2 instance role does not have all policies "
                    "required by the infrastructure architecture."
                ),
                "recommendation": (
                    "Attach the required Systems Manager and ECR read-only "
                    "policies to the EC2 instance role."
                ),
                "missing_policies": sorted(missing_policies),
            }
        )

    return findings
