from typing import Any


def render_report(
    resources_analyzed: int,
    findings: list[dict[str, Any]],
) -> str:
    """Render infrastructure findings as a human-readable report."""

    lines = [
        "Infrastructure Analysis",
        "------------------------",
        "",
        f"Resources analyzed: {resources_analyzed}",
        f"Findings: {len(findings)}",
        "",
    ]

    if not findings:
        lines.extend(
            [
                "No infrastructure issues detected.",
                "",
            ]
        )
        return "\n".join(lines)

    for finding in findings:
        lines.extend(
            [
                f"[{finding.get('severity', 'UNKNOWN')}] "
                f"{finding.get('category', 'GENERAL')}",
                "",
                finding.get("title", "Infrastructure finding"),
                f"Resource: {finding.get('resource', 'unknown')}",
                "",
                finding.get("description", ""),
                "",
                "Recommendation:",
                finding.get("recommendation", ""),
                "",
                "------------------------",
                "",
            ]
        )

    return "\n".join(lines)
