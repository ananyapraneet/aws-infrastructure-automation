from unittest.mock import MagicMock, patch

from openai import RateLimitError

from infra_ai.ai.openai import OpenAIProvider


def test_openai_provider_returns_analysis():
    mock_response = MagicMock()
    mock_response.output_text = "SSH exposure is a security risk."

    with patch(
        "infra_ai.ai.openai.OpenAI"
    ) as mock_openai:
        mock_openai.return_value.responses.create.return_value = mock_response

        provider = OpenAIProvider()
        result = provider.analyze_findings(
            [
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
        )

    assert result == "SSH exposure is a security risk."
    mock_openai.return_value.responses.create.assert_called_once()

def test_openai_provider_handles_quota_error():
    with patch(
        "infra_ai.ai.openai.OpenAI"
    ) as mock_openai:
        mock_openai.return_value.responses.create.side_effect = (
            RateLimitError(
                "Quota exhausted",
                response=MagicMock(status_code=429),
                body={
                    "error": {
                        "code": "insufficient_quota",
                    }
                },
            )
        )

        provider = OpenAIProvider()

        try:
            provider.analyze_findings(
                [
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
            )
        except RuntimeError as exc:
            assert str(exc) == (
                "OpenAI API quota is exhausted. "
                "Add API credits or check your API billing configuration."
            )
        else:
            raise AssertionError("Expected RuntimeError was not raised")

def test_openai_provider_requires_api_key():
    with patch.dict("os.environ", {}, clear=True):
        try:
            OpenAIProvider()
        except ValueError as exc:
            assert str(exc) == (
                "OPENAI_API_KEY environment variable is not set."
            )
        else:
            raise AssertionError("Expected ValueError was not raised")
