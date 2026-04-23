# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Check rule 0."""

import pathlib

import python_import_style._append_rule_error
import python_import_style._prepare_file_context


def _rule_0(
    file_path: pathlib.Path,
    file_context: python_import_style._prepare_file_context._FileContext,
) -> list[str]:
    """Rule 0: Disallow double-leading-underscore names within the package."""
    errors: list[str] = []

    if file_context.in_package:
        for part in file_context.subpackage_parts:
            if part.startswith("__"):
                python_import_style._append_rule_error._append_rule_error(
                    errors,
                    file_path,
                    1,
                    0,
                    "private subpackage name '" + part + "' "
                    "must have a single leading underscore",
                )

        if (
            file_context.is_private_module
            and file_context.module_name.startswith("__")
        ):
            python_import_style._append_rule_error._append_rule_error(
                errors,
                file_path,
                1,
                0,
                (
                    "private module name '" + file_context.module_name + "' "
                    "must have a single leading underscore"
                ),
            )

    return errors
