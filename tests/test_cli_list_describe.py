from click.testing import CliRunner

from configurator.main import main


def test_list_profiles():
    runner = CliRunner()
    result = runner.invoke(main, ["--list-profiles"])

    assert result.exit_code == 0
    assert "Available profiles:" in result.output
    assert "coder_app" in result.output


def test_describe_profile():
    runner = CliRunner()
    result = runner.invoke(main, ["--describe-profile", "coder_app"])

    assert result.exit_code == 0
    assert "Profile: coder_app" in result.output
    assert "Resources:" in result.output
    assert "Image" in result.output


def test_training_profile_not_listed_without_profiles_dir():
    runner = CliRunner()
    result = runner.invoke(main, ["--list-profiles"])

    assert result.exit_code == 0
    assert "training_how_to_app" not in result.output
