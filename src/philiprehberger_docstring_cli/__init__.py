"""Automatically generate CLI interfaces from function signatures and docstrings."""

from __future__ import annotations

import argparse
import inspect
import sys
from collections.abc import Callable
from typing import Any, get_type_hints

__all__ = ["cli", "run"]


def cli(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that makes a function callable from the command line.

    Reads the function's signature, type hints, and docstring to build
    an argparse parser. When the decorated function is called with no
    arguments, it parses sys.argv and runs the function.

    Args:
        func: The function to wrap.

    Returns:
        The decorated function with a `.cli()` method for CLI invocation.
    """
    parser = _build_parser(func)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if args or kwargs:
            return func(*args, **kwargs)
        return _run_parser(func, parser)

    wrapper.__wrapped__ = func  # type: ignore[attr-defined]
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__  # type: ignore[attr-defined]
    wrapper.parser = parser  # type: ignore[attr-defined]
    wrapper.cli = lambda argv=None: _run_parser(func, parser, argv)  # type: ignore[attr-defined]

    return wrapper


def run(func: Callable[..., Any], argv: list[str] | None = None) -> Any:
    """Run a function as a CLI command.

    Args:
        func: Function to run. Does not need the @cli decorator.
        argv: Command-line arguments. Defaults to sys.argv[1:].
    """
    parser = _build_parser(func)
    return _run_parser(func, parser, argv)


def _build_parser(func: Callable[..., Any]) -> argparse.ArgumentParser:
    """Build an ArgumentParser from a function's signature and docstring."""
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or ""
    description = doc.split("\n")[0] if doc else ""

    try:
        hints = get_type_hints(func)
    except Exception:
        hints = {}

    parser = argparse.ArgumentParser(
        prog=func.__name__,
        description=description,
    )

    param_docs = _parse_param_docs(doc)

    for name, param in sig.parameters.items():
        hint = hints.get(name)
        help_text = param_docs.get(name, "")

        if param.default is inspect.Parameter.empty:
            # Positional argument
            kwargs: dict[str, Any] = {"help": help_text}
            if hint is bool:
                kwargs["action"] = "store_true"
                kwargs["default"] = False
                parser.add_argument(f"--{name.replace('_', '-')}", **kwargs)
            else:
                if hint is not None and hint is not inspect.Parameter.empty:
                    kwargs["type"] = hint
                parser.add_argument(name, **kwargs)
        else:
            # Optional argument
            kwargs = {"default": param.default, "help": help_text}
            if hint is bool or isinstance(param.default, bool):
                if param.default is False:
                    kwargs["action"] = "store_true"
                    kwargs.pop("default", None)
                    kwargs["default"] = False
                else:
                    kwargs["action"] = "store_false"
                    kwargs.pop("default", None)
                    kwargs["default"] = True
                    name = f"no-{name}"
                parser.add_argument(f"--{name.replace('_', '-')}", **kwargs)
            else:
                if hint is not None:
                    kwargs["type"] = hint
                parser.add_argument(f"--{name.replace('_', '-')}", **kwargs)

    return parser


def _run_parser(
    func: Callable[..., Any],
    parser: argparse.ArgumentParser,
    argv: list[str] | None = None,
) -> Any:
    """Parse arguments and call the function."""
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    kwargs = {k.replace("-", "_"): v for k, v in vars(args).items()}
    result = func(**kwargs)
    if result is not None:
        print(result)
    return result


def _parse_param_docs(docstring: str) -> dict[str, str]:
    """Extract parameter descriptions from a Google-style docstring."""
    params: dict[str, str] = {}
    lines = docstring.split("\n")
    in_args = False

    for line in lines:
        stripped = line.strip()
        if stripped.lower() in ("args:", "arguments:", "parameters:", "params:"):
            in_args = True
            continue
        if in_args:
            if stripped and not stripped.startswith(" ") and stripped.endswith(":"):
                in_args = False
                continue
            if ":" in stripped and not stripped.startswith(" "):
                # Could be "name: description" or "name (type): description"
                parts = stripped.split(":", 1)
                param_name = parts[0].strip().split("(")[0].strip()
                param_desc = parts[1].strip() if len(parts) > 1 else ""
                params[param_name] = param_desc
            elif not stripped:
                in_args = False

    return params
