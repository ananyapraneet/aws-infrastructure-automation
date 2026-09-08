import json
import subprocess
from pathlib import Path


class TerraformAnalyzer:
    def __init__(self, terraform_dir: Path) -> None:
        self.terraform_dir = terraform_dir

    def load_state(self) -> dict:
        result = subprocess.run(
            ["terraform", "show", "-json"],
            cwd=self.terraform_dir,
            capture_output=True,
            text=True,
            check=True,
        )

        return json.loads(result.stdout)

    def get_resources(self, state: dict) -> list[dict]:
        root_module = state.get("values", {}).get("root_module", {})

        return root_module.get("resources", [])

    def get_resource_summaries(self, state: dict) -> list[dict]:
        resources = self.get_resources(state)

        return [
            {
                "address": resource.get("address"),
                "type": resource.get("type"),
                "name": resource.get("name"),
                "values": resource.get("values", {}),
            }
            for resource in resources
        ]
