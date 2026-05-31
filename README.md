# philiprehberger-docstring-cli

[![Tests](https://github.com/philiprehberger/py-docstring-cli/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-docstring-cli/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-docstring-cli.svg)](https://pypi.org/project/philiprehberger-docstring-cli/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-docstring-cli)](https://github.com/philiprehberger/py-docstring-cli/commits/main)

Automatically generate CLI interfaces from function signatures and docstrings.

## Installation

```bash
pip install philiprehberger-docstring-cli
```

## Usage

### With the `@cli` decorator

```python
from philiprehberger_docstring_cli import cli

@cli
def greet(name: str, count: int = 1, loud: bool = False):
    """Greet someone by name.

    Args:
        name: The person to greet.
        count: Number of times to greet.
        loud: Whether to shout.
    """
    greeting = f"Hello, {name}!"
    if loud:
        greeting = greeting.upper()
    for _ in range(count):
        print(greeting)

# Call from CLI: python greet.py Alice --count 3 --loud
# Or call normally: greet("Alice", count=3, loud=True)
```

The decorated function can still be called normally with arguments. When called
with no arguments, it parses `sys.argv` and runs as a CLI command.

Use `.cli(argv=[...])` to pass explicit arguments:

```python
greet.cli(["Alice", "--count", "2", "--loud"])
```

### With `run()`

For one-off usage without decorating:

```python
from philiprehberger_docstring_cli import run

def add(a: int, b: int):
    """Add two numbers.

    Args:
        a: First number.
        b: Second number.
    """
    return a + b

run(add, ["3", "4"])  # prints 7
```

### Adding `--version`

Pass `version="..."` to `run()` to enable a built-in `--version` flag:

```python
from philiprehberger_docstring_cli import run

def add(a: int, b: int):
    """Add two numbers."""
    return a + b

run(add, version="1.0.0")
# Invoking with --version prints "1.0.0" and exits.
```

### Introspecting commands

Use `command_info(fn)` to inspect a `@cli`-decorated (or plain) function
without invoking it. Useful for building help screens, completion data,
or programmatic command listings.

```python
from philiprehberger_docstring_cli import cli, command_info

@cli
def greet(name: str, count: int = 1):
    """Greet someone by name.

    Args:
        name: The person to greet.
        count: Number of times to greet.
    """
    ...

info = command_info(greet)
# {
#   "name": "greet",
#   "description": "Greet someone by name.",
#   "params": [
#     {"name": "name",  "type": "str", "default": None, "required": True,  "help": "The person to greet."},
#     {"name": "count", "type": "int", "default": 1,    "required": False, "help": "Number of times to greet."},
#   ],
# }
```

## API

| Name            | Description                                               |
| --------------- | --------------------------------------------------------- |
| `cli`           | Decorator that makes a function callable from the CLI.    |
| `run`           | Run any function as a CLI command without decorating it.  |
| `command_info`  | Introspect a function and return its CLI metadata.        |

### `@cli`

- Reads type hints to set argument types (`int`, `float`, `str`, etc.)
- Parameters without defaults become positional arguments
- Parameters with defaults become optional `--flags`
- `bool` parameters become `--flag` / `--no-flag` toggles
- Underscore parameter names are converted to hyphenated flags (`dry_run` -> `--dry-run`)
- Google-style docstring `Args:` sections are used for help text

### `run(func, argv=None, *, version=None)`

- Builds a parser from the function and parses the given `argv` (or `sys.argv[1:]`)
- Does not require the `@cli` decorator
- `version`: when set, the parser accepts `--version` and prints this string

### `command_info(func)`

- Returns a dict with `name`, `description`, and `params`
- Each entry in `params` is a dict with `name`, `type`, `default`, `required`, and `help`
- Works on `@cli`-decorated functions as well as plain functions

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-docstring-cli)

🐛 [Report issues](https://github.com/philiprehberger/py-docstring-cli/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-docstring-cli/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
