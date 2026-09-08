from typing import Any

from infra_ai.analyzer.analyzer import analyze_resources


def validate_resources(
    resources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Validate infrastructure resources using deterministic checks."""

    return analyze_resources(resources)
