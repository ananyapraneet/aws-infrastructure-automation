from infra_ai.ai.base import AIProvider
from infra_ai.troubleshoot.troubleshooter import troubleshoot_file


class FakeAIProvider(AIProvider):
    def __init__(self) -> None:
        self.received_findings = []

    def analyze_findings(self, findings):
        self.received_findings = findings
        return "Mock troubleshooting analysis."


def test_troubleshoot_file_uses_diagnostic_content() -> None:
    provider = FakeAIProvider()

    result = troubleshoot_file(
        provider=provider,
        file_path="deployment-error.txt",
        content="Failed to pull image from ECR.",
    )

    assert result == "Mock troubleshooting analysis."
    assert len(provider.received_findings) == 1

    finding = provider.received_findings[0]

    assert finding["category"] == "TROUBLESHOOTING"
    assert finding["resource"] == "deployment-error.txt"
    assert "Failed to pull image from ECR." in finding["description"]
    assert "deployment-error.txt" in finding["description"]


def test_troubleshoot_file_includes_diagnostic_safety_rules() -> None:
    provider = FakeAIProvider()

    troubleshoot_file(
        provider=provider,
        file_path="deployment-error.txt",
        content="Container failed to start.",
    )

    prompt = provider.received_findings[0]["description"]

    assert "source of truth" in prompt
    assert "Do not invent infrastructure resources, errors, or configuration." in prompt
    assert "Clearly distinguish evidence from inference." in prompt
    assert "Do not claim certainty when the evidence is insufficient." in prompt
    assert "Do not execute commands." in prompt
    assert "Do not suggest automatically modifying infrastructure." in prompt
