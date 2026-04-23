# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Check rule 3."""

import ast
import pathlib

import python_import_style._append_rule_error
import python_import_style._prepare_file_context


def _rule_3(
    file_path: pathlib.Path,
    file_context: python_import_style._prepare_file_context._FileContext,
    tree: ast.AST,
) -> list[str]:
    """Rule 3: Forbid relative imports inside the package."""
    errors: list[str] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ImportFrom)
            and file_context.in_package
            and node.level > 0
        ):
            python_import_style._append_rule_error._append_rule_error(
                errors,
                file_path,
                node.lineno,
                3,
                "relative imports are forbidden inside the package",
            )
    return errors
