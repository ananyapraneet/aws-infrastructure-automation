import argparse
from pathlib import Path

from infra_ai.troubleshoot.troubleshooter import troubleshoot_file
from infra_ai.ai.openai import OpenAIProvider
from infra_ai.validation.validator import validate_resources
from infra_ai.analyzer.analyzer import analyze_resources
from infra_ai.analyzer.test_data import get_controlled_findings
from infra_ai.analyzer.terraform import TerraformAnalyzer
from infra_ai.explain.explainer import explain_file
from infra_ai.inputs.files import read_text_file
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

def validate() -> None:
    """Validate Terraform infrastructure using deterministic checks."""

    project_root = Path.cwd()
    terraform_dir = project_root / "terraform"

    if not terraform_dir.is_dir():
        print("Infrastructure Validation")
        print("-------------------------")
        print("Terraform directory not found.")
        print(f"Expected: {terraform_dir}")
        return

    analyzer = TerraformAnalyzer(terraform_dir)

    try:
        state = analyzer.load_state()
    except Exception as exc:
        print("Infrastructure Validation")
        print("-------------------------")
        print("Failed to read Terraform state.")
        print(f"Error: {exc}")
        return

    resources = analyzer.get_resource_summaries(state)
    findings = validate_resources(resources)

    print("Infrastructure Validation")
    print("-------------------------")
    print()
    print(f"Resources validated: {len(resources)}")
    print("Checks performed: 4")
    print(f"Findings: {len(findings)}")
    print()

    if findings:
        print("Validation: FAILED")
        print()
        print(render_report(len(resources), findings))
        return

    print("Validation: PASSED")
    print("No infrastructure validation issues detected.")

def explain_file_command(file_path: str) -> None:
    """Explain an infrastructure-related file using AI."""

    try:
        content = read_text_file(file_path)
    except (FileNotFoundError, ValueError) as exc:
        print("Infrastructure Explanation")
        print("--------------------------")
        print(f"Error: {exc}")
        return

    print("Infrastructure Explanation")
    print("--------------------------")
    print(f"File: {file_path}")
    print()

    try:
        provider = OpenAIProvider()
        explanation = explain_file(
            provider=provider,
            file_path=file_path,
            content=content,
        )
    except RuntimeError as exc:
        print("Unable to generate AI explanation.")
        print(f"Error: {exc}")
        return

    print(explanation)

def troubleshoot_file_command(file_path: str) -> None:
    """Troubleshoot an infrastructure or deployment diagnostic file using AI."""

    try:
        content = read_text_file(file_path)
    except (FileNotFoundError, ValueError) as exc:
        print("Infrastructure Troubleshooting")
        print("-------------------------------")
        print(f"Error: {exc}")
        return

    print("Infrastructure Troubleshooting")
    print("-------------------------------")
    print(f"File: {file_path}")
    print()

    try:
        provider = OpenAIProvider()
        analysis = troubleshoot_file(
            provider=provider,
            file_path=file_path,
            content=content,
        )
    except RuntimeError as exc:
        print("Unable to generate AI troubleshooting analysis.")
        print(f"Error: {exc}")
        return

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

    explain_parser = subparsers.add_parser(
        "explain",
        help="Explain an infrastructure-related file using AI.",
    )

    explain_parser.add_argument(
        "file",
        help="Path to the infrastructure file to explain.",
    )

    troubleshoot_parser = subparsers.add_parser(
        "troubleshoot",
        help="Troubleshoot an infrastructure or deployment diagnostic file using AI.",
    )

    troubleshoot_parser.add_argument(
        "file",
        help="Path to the diagnostic file to troubleshoot.",
    )

    subparsers.add_parser(
        "validate",
        help="Validate Terraform infrastructure.",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        if args.test and not args.ai:
            analyze_parser.error("--test requires --ai")

        analyze(
            use_ai=args.ai,
            test_mode=args.test,
        )

    elif args.command == "explain":
        explain_file_command(args.file)

    elif args.command == "troubleshoot":
        troubleshoot_file_command(args.file)

    elif args.command == "validate":
        validate()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
