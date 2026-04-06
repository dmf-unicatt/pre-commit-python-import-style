# Python Import Style Hook

This repository provides a pre-commit compatible hook that enforces opinionated import style rules, namely requiring to use `import ...` everywhere, except for `__init__.py` files in your package in which `from ... import ...` is allowed only for your package namespace.

## Hook Entry Point

```bash
python -m python_import_style
```

## Command Line Options

```text
--root-dir PATH             Project root directory (default: current directory)
--package-dir-prefix PATH   Parent directory of the package, relative to the project root (default: empty)
--package-name NAME         Package name to validate
--tests-dir NAME            Tests directory to validate (default: tests)
```

## Integration with prek

This repository exposes the hook in `.pre-commit-hooks.yaml` with id `python-import-style`.

Example configuration:

```toml
[[repos]]
repo = "https://github.com/dmf-unicatt/pre-commit-python-import-style"
rev = "<tag-or-sha>"
hooks = [
    {
        id = "python-import-style",
        args = [
            "--root-dir", "subdirectory_with_python_code",   # omit if "."
            "--package-dir-prefix", "src",  # omit if flatten layout
            "--package-name", "my_package",
            "--tests-dir", "tests"  # defaults to tests
        ]
    },
]
```
