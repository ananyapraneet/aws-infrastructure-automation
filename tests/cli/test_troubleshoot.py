from infra_ai.cli import main


def test_troubleshoot_file_command_success(
    monkeypatch,
    capsys,
) -> None:
    def fake_read_text_file(file_path):
        assert file_path == "tests/fixtures/deployment-error.txt"
        return "Failed to pull image from ECR."

    class FakeProvider:
        pass

    def fake_openai_provider():
        return FakeProvider()

    def fake_troubleshoot_file(provider, file_path, content):
        assert isinstance(provider, FakeProvider)
        assert file_path == "tests/fixtures/deployment-error.txt"
        assert content == "Failed to pull image from ECR."
        return "Mock troubleshooting analysis."

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
        "troubleshoot_file",
        fake_troubleshoot_file,
    )

    main.troubleshoot_file_command("tests/fixtures/deployment-error.txt")

    output = capsys.readouterr().out

    assert "Infrastructure Troubleshooting" in output
    assert "File: tests/fixtures/deployment-error.txt" in output
    assert "Mock troubleshooting analysis." in output


def test_troubleshoot_file_command_handles_input_error(
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

    main.troubleshoot_file_command("missing.txt")

    output = capsys.readouterr().out

    assert "Infrastructure Troubleshooting" in output
    assert "Input file not found: missing.txt" in output


def test_troubleshoot_file_command_handles_ai_error(
    monkeypatch,
    capsys,
) -> None:
    def fake_read_text_file(file_path):
        return "Container failed to start."

    class FakeProvider:
        pass

    def fake_openai_provider():
        return FakeProvider()

    def fake_troubleshoot_file(provider, file_path, content):
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
        "troubleshoot_file",
        fake_troubleshoot_file,
    )

    main.troubleshoot_file_command("tests/fixtures/deployment-error.txt")

    output = capsys.readouterr().out

    assert "Unable to generate AI troubleshooting analysis." in output
    assert "AI service unavailable." in output
