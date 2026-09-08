from typing import Any


REQUIRED_PRIVATE_ENDPOINTS = {
    "com.amazonaws.ap-south-1.ecr.api",
    "com.amazonaws.ap-south-1.ecr.dkr",
    "com.amazonaws.ap-south-1.ssm",
    "com.amazonaws.ap-south-1.ssmmessages",
    "com.amazonaws.ap-south-1.s3",
}


def find_missing_private_endpoints(
    resources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    findings = []

    has_ec2_instance = any(
        resource.get("type") == "aws_instance"
        for resource in resources
    )

    if not has_ec2_instance:
        return []

    configured_endpoints = {
        resource.get("values", {}).get("service_name")
        for resource in resources
        if resource.get("type") == "aws_vpc_endpoint"
    }

    missing_endpoints = REQUIRED_PRIVATE_ENDPOINTS - configured_endpoints

    if not missing_endpoints:
        return []

    return [
        {
            "severity": "HIGH",
            "category": "NETWORK",
            "resource": "aws_vpc_endpoint",
            "title": "Required private VPC endpoints are missing",
            "description": (
                "Private infrastructure may not have connectivity to "
                "required AWS services without public internet access."
            ),
            "recommendation": (
                "Configure the required VPC endpoints for Systems Manager, "
                "ECR, and S3."
            ),
            "missing_endpoints": sorted(missing_endpoints),
        }
    ]
