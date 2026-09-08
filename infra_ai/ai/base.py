from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Provider-neutral interface for AI infrastructure analysis."""

    @abstractmethod
    def analyze_findings(
        self,
        findings: list[dict[str, Any]],
    ) -> str:
        """Explain infrastructure findings and provide recommendations."""
        raise NotImplementedError
