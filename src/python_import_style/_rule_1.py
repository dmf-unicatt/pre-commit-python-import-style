# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Check rule 1."""

import ast
import pathlib

import python_import_style._append_rule_error
import python_import_style._prepare_file_context


def _rule_1(
    package_name: str,
    file_path: pathlib.Path,
    file_context: python_import_style._prepare_file_context._FileContext,
    tree: ast.AST,
) -> list[str]:
    """Rule 1: Forbid `from ... import ...` outside package `__init__.py`.

    It skips ImportFrom nodes that are relative imports inside the package
    because those are handled by Rule 3.
    """
    errors: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            if file_context.in_package and node.level > 0:
                # Relative imports are handled by Rule 3; skip them to avoid
                # duplicate reports.
                assert module is None
                continue
            if not file_context.is_init:
                python_import_style._append_rule_error._append_rule_error(
                    errors,
                    file_path,
                    node.lineno,
                    1,
                    "use 'import ...' instead of 'from ... import ...'",
                )
            else:
                assert module is not None  # relative imports are continued
                if module == package_name or module.startswith(
                    package_name + "."
                ):
                    if any(alias.name == "*" for alias in node.names):
                        python_import_style._append_rule_error._append_rule_error(
                            errors,
                            file_path,
                            node.lineno,
                            1,
                            (
                                "wildcard imports (from ... import *) "
                                "are not allowed in __init__.py"
                            ),
                        )
                else:
                    python_import_style._append_rule_error._append_rule_error(
                        errors,
                        file_path,
                        node.lineno,
                        1,
                        (
                            "in __init__.py, only use the syntax "
                            "'from ... import ...' to import from the package "
                            "itself, its subpackages or its submodules"
                        ),
                    )
    return errors
