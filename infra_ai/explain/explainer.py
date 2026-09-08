from typing import Any

from infra_ai.ai.base import AIProvider


def explain_file(
    provider: AIProvider,
    file_path: str,
    content: str,
) -> str:
    """Explain the contents of an infrastructure-related file."""

    prompt = f"""
Explain the following infrastructure file.

File: {file_path}

Provide:

1. A concise summary of what the file does.
2. The main infrastructure components or configuration it defines.
3. Important security or reliability considerations.
4. Any potential configuration concerns.
5. Practical recommendations where appropriate.

Rules:

- Treat the provided file contents as the source of truth.
- Do not invent resources, configuration, or behavior.
- Do not execute commands.
- Do not suggest automatically modifying infrastructure.
- Clearly distinguish observed configuration from recommendations.
- Keep the explanation concise and understandable.

File contents:

{content}
""".strip()

    return provider.analyze_findings(
        [
            {
                "category": "EXPLANATION",
                "resource": file_path,
                "title": "Infrastructure file explanation",
                "description": prompt,
                "recommendation": (
                    "Provide a clear explanation based only on the supplied "
                    "file contents."
                ),
            }
        ]
    )
