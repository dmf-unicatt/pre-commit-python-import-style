# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Check rule 2."""

import ast
import pathlib

import python_import_style._append_rule_error

_ALLOWED_IMPORT_ALIASES: dict[str, str] = {
    "numpy": "np",
    "numpy.typing": "npt",
    "pandas": "pd",
}


def _is_allowed_import_alias(module_name: str, alias_name: str) -> bool:
    """Return True if `alias_name` is a permitted alias for `module_name`."""
    expected = _ALLOWED_IMPORT_ALIASES.get(module_name)
    return expected == alias_name


def _rule_2(
    file_path: pathlib.Path,
    tree: ast.AST,
) -> list[str]:
    """Rule 2: Disallow import aliases except curated top-level aliases.

    - For `import X as Y`, curated aliases like `numpy as np` are permitted.
    - For `from ... import ... as ...`, aliases are generally forbidden.
    """
    errors: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.asname is not None:
                    python_import_style._append_rule_error._append_rule_error(
                        errors,
                        file_path,
                        node.lineno,
                        2,
                        "from ... import ... aliases are forbidden",
                    )
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if alias.asname is not None and not _is_allowed_import_alias(
                    name, alias.asname
                ):
                    python_import_style._append_rule_error._append_rule_error(
                        errors,
                        file_path,
                        node.lineno,
                        2,
                        (
                            "import aliases are forbidden, except for "
                            "a curated list of aliases"
                        ),
                    )
    return errors
