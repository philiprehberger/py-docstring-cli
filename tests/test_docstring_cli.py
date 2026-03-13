from __future__ import annotations

import pytest

from philiprehberger_docstring_cli import cli, run


def test_positional_args_parsed() -> None:
    @cli
    def greet(name: str) -> str:
        """Greet someone."""
        return f"Hello, {name}!"

    result = greet.cli(["Alice"])
    assert result == "Hello, Alice!"


def test_optional_args_with_defaults() -> None:
    @cli
    def repeat(word: str, count: int = 3) -> str:
        """Repeat a word."""
        return " ".join([word] * count)

    result = repeat.cli(["hi", "--count", "2"])
    assert result == "hi hi"


def test_optional_args_use_default_when_omitted() -> None:
    @cli
    def repeat(word: str, count: int = 3) -> str:
        """Repeat a word."""
        return " ".join([word] * count)

    result = repeat.cli(["hi"])
    assert result == "hi hi hi"


def test_bool_flag_default_false() -> None:
    @cli
    def shout(msg: str, loud: bool = False) -> str:
        """Shout a message."""
        return msg.upper() if loud else msg

    assert shout.cli(["hello"]) == "hello"
    assert shout.cli(["hello", "--loud"]) == "HELLO"


def test_type_conversion_int() -> None:
    @cli
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    result = add.cli(["3", "4"])
    assert result == 7


def test_type_conversion_float() -> None:
    @cli
    def multiply(x: float, y: float) -> float:
        """Multiply two floats."""
        return x * y

    result = multiply.cli(["2.5", "4.0"])
    assert result == 10.0


def test_help_text_from_docstring() -> None:
    @cli
    def example(name: str) -> str:
        """Do something cool.

        Args:
            name: The name to use.
        """
        return name

    actions = example.parser._actions  # type: ignore[attr-defined]
    name_action = [a for a in actions if "name" in a.dest][0]
    assert name_action.help == "The name to use."


def test_run_without_decorator() -> None:
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    result = run(add, ["10", "20"])
    assert result == 30


def test_cli_preserves_direct_call() -> None:
    @cli
    def add(a: int, b: int) -> int:
        """Add numbers."""
        return a + b

    result = add(3, 5)
    assert result == 8


def test_multiple_positional_args() -> None:
    @cli
    def concat(first: str, second: str, third: str) -> str:
        """Concatenate three strings."""
        return f"{first}-{second}-{third}"

    result = concat.cli(["a", "b", "c"])
    assert result == "a-b-c"


def test_underscore_to_hyphen_flag() -> None:
    @cli
    def deploy(target: str, dry_run: bool = False) -> str:
        """Deploy something.

        Args:
            target: Where to deploy.
            dry_run: Perform a dry run.
        """
        return f"{'DRY ' if dry_run else ''}deploy to {target}"

    result = deploy.cli(["prod", "--dry-run"])
    assert result == "DRY deploy to prod"


def test_result_printed_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    @cli
    def say(word: str) -> str:
        """Say a word."""
        return word

    say.cli(["hello"])
    captured = capsys.readouterr()
    assert "hello" in captured.out


def test_no_args_function() -> None:
    @cli
    def noop() -> str:
        """Do nothing."""
        return "done"

    result = noop.cli([])
    assert result == "done"


def test_cli_with_explicit_argv() -> None:
    @cli
    def echo(msg: str, times: int = 1) -> str:
        """Echo a message."""
        return " ".join([msg] * times)

    result = echo.cli(argv=["world", "--times", "2"])
    assert result == "world world"
