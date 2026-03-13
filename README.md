# philiprehberger-docstring-cli

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

## API

| Name   | Description                                               |
| ------ | --------------------------------------------------------- |
| `cli`  | Decorator that makes a function callable from the CLI.    |
| `run`  | Run any function as a CLI command without decorating it.  |

### `@cli`

- Reads type hints to set argument types (`int`, `float`, `str`, etc.)
- Parameters without defaults become positional arguments
- Parameters with defaults become optional `--flags`
- `bool` parameters become `--flag` / `--no-flag` toggles
- Underscore parameter names are converted to hyphenated flags (`dry_run` -> `--dry-run`)
- Google-style docstring `Args:` sections are used for help text

### `run(func, argv=None)`

- Builds a parser from the function and parses the given `argv` (or `sys.argv[1:]`)
- Does not require the `@cli` decorator

## License

MIT
