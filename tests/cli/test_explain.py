from infra_ai.cli import main


def test_explain_file_command_success(
    monkeypatch,
    capsys,
) -> None:
    def fake_read_text_file(file_path):
        assert file_path == "terraform/ec2.tf"
        return 'resource "aws_instance" "app" {}'

    class FakeProvider:
        pass

    def fake_openai_provider():
        return FakeProvider()

    def fake_explain_file(provider, file_path, content):
        assert isinstance(provider, FakeProvider)
        assert file_path == "terraform/ec2.tf"
        assert content == 'resource "aws_instance" "app" {}'
        return "Mock infrastructure explanation."

    monkeypatch.setattr(
        main,
        "read_text_file",
        fake_read_text_file,
    )
    monkeypatch.setattr(
        main,
        "OpenAIProvider",
        fake_openai_provider,
    )
    monkeypatch.setattr(
        main,
        "explain_file",
        fake_explain_file,
    )

    main.explain_file_command("terraform/ec2.tf")

    output = capsys.readouterr().out

    assert "Infrastructure Explanation" in output
    assert "File: terraform/ec2.tf" in output
    assert "Mock infrastructure explanation." in output


def test_explain_file_command_handles_input_error(
    monkeypatch,
    capsys,
) -> None:
    def fake_read_text_file(file_path):
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    monkeypatch.setattr(
        main,
        "read_text_file",
        fake_read_text_file,
    )

    main.explain_file_command("missing.tf")

    output = capsys.readouterr().out

    assert "Infrastructure Explanation" in output
    assert "Input file not found: missing.tf" in output


def test_explain_file_command_handles_ai_error(
    monkeypatch,
    capsys,
) -> None:
    def fake_read_text_file(file_path):
        return "test infrastructure configuration"

    class FakeProvider:
        pass

    def fake_openai_provider():
        return FakeProvider()

    def fake_explain_file(provider, file_path, content):
        raise RuntimeError("AI service unavailable.")

    monkeypatch.setattr(
        main,
        "read_text_file",
        fake_read_text_file,
    )
    monkeypatch.setattr(
        main,
        "OpenAIProvider",
        fake_openai_provider,
    )
    monkeypatch.setattr(
        main,
        "explain_file",
        fake_explain_file,
    )

    main.explain_file_command("terraform/ec2.tf")

    output = capsys.readouterr().out

    assert "Unable to generate AI explanation." in output
    assert "AI service unavailable." in output
