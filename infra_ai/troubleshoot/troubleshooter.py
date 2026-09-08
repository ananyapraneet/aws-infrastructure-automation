from infra_ai.ai.base import AIProvider


def troubleshoot_file(
    provider: AIProvider,
    file_path: str,
    content: str,
) -> str:
    """Analyze an error or diagnostic file and provide troubleshooting guidance."""

    prompt = f"""
Analyze the following infrastructure or deployment diagnostic file.

File: {file_path}

Provide:

1. The most likely cause of the reported problem.
2. Evidence from the provided content supporting that diagnosis.
3. Other plausible causes if the evidence is insufficient.
4. Practical checks that could confirm the diagnosis.
5. A recommended resolution approach.

Rules:

- Treat the provided diagnostic content as the source of truth.
- Do not invent infrastructure resources, errors, or configuration.
- Clearly distinguish evidence from inference.
- Do not claim certainty when the evidence is insufficient.
- Do not execute commands.
- Do not suggest automatically modifying infrastructure.
- Do not assume access to systems that are not represented in the provided content.
- Keep the troubleshooting analysis concise and actionable.

Diagnostic content:

{content}
""".strip()

    return provider.analyze_findings(
        [
            {
                "category": "TROUBLESHOOTING",
                "resource": file_path,
                "title": "Infrastructure troubleshooting request",
                "description": prompt,
                "recommendation": (
                    "Diagnose the reported problem using only the supplied "
                    "diagnostic content."
                ),
            }
        ]
    )
