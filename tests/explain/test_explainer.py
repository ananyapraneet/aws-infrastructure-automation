from infra_ai.ai.base import AIProvider
from infra_ai.explain.explainer import explain_file


class FakeAIProvider(AIProvider):
    def __init__(self) -> None:
        self.received_findings = []

    def analyze_findings(self, findings):
        self.received_findings = findings
        return "Mock infrastructure explanation."


def test_explain_file_uses_file_content() -> None:
    provider = FakeAIProvider()

    result = explain_file(
        provider=provider,
        file_path="terraform/main.tf",
        content='resource "aws_vpc" "main" {}',
    )

    assert result == "Mock infrastructure explanation."
    assert len(provider.received_findings) == 1

    finding = provider.received_findings[0]

    assert finding["category"] == "EXPLANATION"
    assert finding["resource"] == "terraform/main.tf"
    assert "aws_vpc" in finding["description"]
    assert "terraform/main.tf" in finding["description"]


def test_explain_file_includes_safety_rules() -> None:
    provider = FakeAIProvider()

    explain_file(
        provider=provider,
        file_path="terraform/main.tf",
        content='resource "aws_vpc" "main" {}',
    )

    prompt = provider.received_findings[0]["description"]

    assert "Do not execute commands." in prompt
    assert "Do not suggest automatically modifying infrastructure." in prompt
    assert "source of truth" in prompt
