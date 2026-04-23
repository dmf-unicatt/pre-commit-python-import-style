# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Return the AST tree for a given file."""

import ast
import pathlib

import python_import_style._append_rule_error
import python_import_style._is_python_file


def _get_tree_from_file(
    file_path: pathlib.Path,
) -> tuple[ast.AST | None, list[str]]:
    """Return the AST tree for `file_path`."""
    errors: list[str] = []
    assert file_path.is_absolute(), "File paths must be absolute"

    try:
        source = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        python_import_style._append_rule_error._append_rule_error(
            errors,
            file_path,
            1,
            None,
            f"cannot read file: {exc}",
        )
        return None, errors

    if not python_import_style._is_python_file._is_python_file(file_path):
        python_import_style._append_rule_error._append_rule_error(
            errors,
            file_path,
            1,
            None,
            "not a python file",
        )
        return None, errors

    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as exc:
        line = exc.lineno or 1
        python_import_style._append_rule_error._append_rule_error(
            errors,
            file_path,
            line,
            None,
            "syntax error while parsing file",
        )
        return None, errors

    return tree, errors
