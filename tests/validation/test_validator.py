from infra_ai.validation.validator import validate_resources


def test_validate_resources_returns_no_findings_for_secure_resources() -> None:
    resources = [
        {
            "address": "aws_security_group.alb",
            "type": "aws_security_group",
            "name": "alb",
            "values": {
                "ingress": [
                    {
                        "protocol": "tcp",
                        "from_port": 80,
                        "to_port": 80,
                        "cidr_blocks": ["0.0.0.0/0"],
                    }
                ]
            },
        }
    ]

    findings = validate_resources(resources)

    assert findings == []


def test_validate_resources_detects_public_ssh_exposure() -> None:
    resources = [
        {
            "address": "aws_security_group.insecure",
            "type": "aws_security_group",
            "name": "insecure",
            "values": {
                "ingress": [
                    {
                        "protocol": "tcp",
                        "from_port": 22,
                        "to_port": 22,
                        "cidr_blocks": ["0.0.0.0/0"],
                    }
                ]
            },
        }
    ]

    findings = validate_resources(resources)

    assert len(findings) == 1
    assert findings[0]["severity"] == "HIGH"
    assert findings[0]["category"] == "SECURITY"
    assert findings[0]["title"] == "SSH exposed to the internet"
