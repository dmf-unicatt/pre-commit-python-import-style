# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._check_rule_0."""

import pathlib

import test_utils

import python_import_style._prepare_file_context
import python_import_style._rule_0


def _run_rule_0_for_file(
    package_name: str,
    package_root: pathlib.Path,
    tests_root: pathlib.Path,
    file_path: pathlib.Path,
) -> list[str]:
    """Run rule 0 for a file and return the list of error messages."""
    file_context, _ = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name,
            package_root,
            tests_root,
            file_path,
        )
    )
    assert file_context is not None

    return python_import_style._rule_0._rule_0(
        file_path,
        file_context,
    )


def test_rule_0_forbids_double_leading_underscore_in_module(
    tmp_path: pathlib.Path,
) -> None:
    """Reject private module filenames that start with two underscores."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "__mod.py"
    mod.write_text("import os\n", encoding="utf-8")

    errors = _run_rule_0_for_file(package_name, package_root, tests_root, mod)
    test_utils._assert_rule_errors(errors, [(0, "private module name", 1)])


def test_rule_0_forbids_double_leading_underscore_in_subpackage(
    tmp_path: pathlib.Path,
) -> None:
    """Reject subpackage directory names starting with two underscores."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "__subpkg" / "_mod.py"
    mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    errors = _run_rule_0_for_file(package_name, package_root, tests_root, mod)
    test_utils._assert_rule_errors(errors, [(0, "private subpackage name", 1)])
