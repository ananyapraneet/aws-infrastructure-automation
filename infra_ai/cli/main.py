import argparse
from pathlib import Path

from infra_ai.ai.openai import OpenAIProvider
from infra_ai.analyzer.analyzer import analyze_resources
from infra_ai.analyzer.test_data import get_controlled_findings
from infra_ai.analyzer.terraform import TerraformAnalyzer
from infra_ai.reporting.report import render_report


def analyze(use_ai: bool = False, test_mode: bool = False) -> None:
    if test_mode:
        findings = get_controlled_findings()
        resources_analyzed = 1
        print("Test mode: controlled findings")
    else:
        project_root = Path.cwd()
        terraform_dir = project_root / "terraform"

        if not terraform_dir.is_dir():
            print("Infrastructure Analysis")
            print("------------------------")
            print("Terraform directory not found.")
            print(f"Expected: {terraform_dir}")
            return

        analyzer = TerraformAnalyzer(terraform_dir)

        try:
            state = analyzer.load_state()
        except Exception as exc:
            print("Infrastructure Analysis")
            print("------------------------")
            print("Failed to read Terraform state.")
            print(f"Error: {exc}")
            return

        resources = analyzer.get_resource_summaries(state)
        findings = analyze_resources(resources)
        resources_analyzed = len(resources)

    print(render_report(resources_analyzed, findings))

    if use_ai and findings:
        try:
            provider = OpenAIProvider()
            analysis = provider.analyze_findings(findings)
        except RuntimeError as exc:
            print("AI Analysis")
            print("-----------")
            print("Unable to generate AI analysis.")
            print(f"Error: {exc}")
            return

        print("AI Analysis")
        print("-----------")
        print(analysis)

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="infra-ai",
        description="AI-assisted AWS infrastructure analysis tool.",
    )

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze Terraform infrastructure.",
    )

    analyze_parser.add_argument(
        "--ai",
        action="store_true",
        help="Generate AI explanations for infrastructure findings.",
    )

    analyze_parser.add_argument(
        "--test",
        action="store_true",
        help="Use controlled findings for AI integration testing.",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        if args.test and not args.ai:
            analyze_parser.error("--test requires --ai")

        analyze(
            use_ai=args.ai,
            test_mode=args.test,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
