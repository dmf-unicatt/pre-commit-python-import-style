# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Check files against all rules."""

import pathlib
import typing

import python_import_style._get_tree_from_file
import python_import_style._iter_project_python_files
import python_import_style._prepare_file_context
import python_import_style._rule_0

if typing.TYPE_CHECKING:
    import ast


def check_all_rules(
    package_name: str,
    project_root: pathlib.Path,
    package_root: pathlib.Path,
    tests_root: pathlib.Path,
    file_paths: list[pathlib.Path],
) -> list[str]:
    """Check files against all rules and return errors."""
    errors: list[str] = []

    # Get AST trees and file contexts for all files in the project root.
    # Note that it would not be correct to only get the trees and contexts
    # for the files being checked (input argument `file_paths`), because
    # some rules may need the trees and contexts of other files in the project,
    # even if those files are not being checked themselves.
    trees: dict[pathlib.Path, ast.AST] = {}
    file_contexts: dict[
        pathlib.Path, python_import_style._prepare_file_context._FileContext
    ] = {}
    for file_path in python_import_style._iter_project_python_files._iter_project_python_files(  # noqa: E501
        project_root
    ):
        tree, tree_errors = (
            python_import_style._get_tree_from_file._get_tree_from_file(
                file_path
            )
        )
        if tree is None:  # pragma: no cover
            errors.extend(tree_errors)
            continue
        trees[file_path] = tree

        file_context, file_context_errors = (
            python_import_style._prepare_file_context._prepare_file_context(
                package_name, package_root, tests_root, file_path
            )
        )
        if file_context is None:  # pragma: no cover
            errors.extend(file_context_errors)
            continue
        file_contexts[file_path] = file_context

    # Check all rules for all files which are being checked.
    for file_path in file_paths:
        tree = trees.get(file_path)
        file_context = file_contexts.get(file_path)
        if tree is None or file_context is None:  # pragma: no cover
            continue

        errors.extend(
            python_import_style._rule_0._rule_0(
                file_path,
                file_context,
            )
        )
    return errors
