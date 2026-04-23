# Python Import Style Hook

This repository provides a pre-commit hook that enforces an opinionated
import-style policy.

## Name conventions
In the following we refer to:
- package, e.g. `my_package` in the directory `my_package/`, with public API defined by the file `my_package/__init__.py`;
- public subpackages, e.g. `my_package.public_subpackage` in the directory `my_package/public_subpackage`, with public API defined by the file `my_package/public_subpackage/__init__.py`;
- private subpackages, e.g. `my_package._private_subpackage` in the directory `my_package/_private_subpackage`, with public API defined by the file `my_package/_private_subpackage/__init__.py`;
- public modules of a public (sub)package, e.g. `my_package.public_subpackage.public_module` in the file `my_package/public_subpackage/public_module.py`
- private modules of a public (sub)package, e.g. `my_package.public_subpackage._private_module` in the file `my_package/public_subpackage/_private_module.py`
- private modules of a private subpackage, e.g. `my_package._private_subpackage._private_module` in the file `my_package/_private_subpackage/_private_module.py`


## Rules
- Rule 0: all private subpackages and private modules must have a single leading underscore `_` in their name. Private subpackages and private modules with multiple leading underscores `__` are not allowed, except for `__init__.py` files, which define the public API of the (sub)package, and `__main__.py` files, which define the entry point of the (sub)package; due to their special role, the latter files are not considered private modules.
- Rule 1: the style `from <module_or_package> import <name>` is generally forbidden. Instead, use `import <module_or_package>`. Exception: the `from <module_or_subpackage> import <name>` syntax is only allowed in `__init__.py`, but just to populate the public API of the (sub)package, and never with `from <module_or_subpackage> import *`.
- Rule 2: import aliases are generally not allowed. Exception: a curated list of well-known external libraries may be imported using their customary aliases (for instance, `import numpy as np` or `import pandas as pd`).
- Rule 3: within the package, using relative imports is forbidden. Instead, use fully qualified import names.
- Rule 4: a private subpackage or a private module must not depend on the public API of its enclosing package. It must instead import directly from the private modules where the required names are defined.
- Rule 5: a private subpackage must not have public modules.
- Rule 6: a name is allowed to be part of the public API only if it is used by subpackages or modules outside of the defining subpackage, or by external code (excluding code within the tests).
- Rule 7: any name that is part of the public API must not start with a leading underscore `_`. Conversely, any name that is not part of the public API must start with a leading underscore `_`.
- Rule 8: a public module must not be re-exported through the public API of its package. External code must import names directly from the public module itself. This rule also applies to subpackages: do not re-export them via `__init__.py`; import directly from the subpackage.
- Rule 9: external code (excluding code within the tests) must not access private subpackages or modules. Only the public API of each subpackage or module must be used by external code. Exception: code within the tests may access private subpackages or private modules, but only for names that are not exposed through the public API. All names in the public API must be exercised by tests via public imports only, not by importing private modules directly.
- Rule 10: anything that is imported in a `__init__.py` file is automatically considered part of the public API of that (sub)package. Therefore, it is not necessary to define `__all__` in `__init__.py`. In fact, `__all__` must not be defined at all.
- Rule 11: all names defined in `__init__.py` files must be defined exclusively via import statements from modules; no local definitions (functions, classes, constants) are allowed.

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
rev = "31f5807d9d4915b53a44220fa82b8bed8b0e1f7c"
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
