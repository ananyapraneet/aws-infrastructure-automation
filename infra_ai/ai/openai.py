import os
from typing import Any

from openai import APIError, OpenAI, RateLimitError

from infra_ai.ai.base import AIProvider
from infra_ai.ai.prompts import build_analysis_prompt


class OpenAIProvider(AIProvider):
    """OpenAI implementation of the AI provider interface."""

    def __init__(self, model: str | None = None) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")

    def analyze_findings(
        self,
        findings: list[dict[str, Any]],
    ) -> str:
        prompt = build_analysis_prompt(findings)

        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=(
                    "You are an infrastructure security and reliability "
                    "assistant. Analyze the provided infrastructure findings. "
                    "Do not modify infrastructure or execute commands. "
                    "Provide clear explanations and practical recommendations."
                ),
                input=prompt,
            )

            return response.output_text

        except RateLimitError as exc:
            raise RuntimeError(
                "OpenAI API quota is exhausted. "
                "Add API credits or check your API billing configuration."
            ) from exc

        except APIError as exc:
            raise RuntimeError(
                f"OpenAI API request failed: {exc}"
            ) from exc
