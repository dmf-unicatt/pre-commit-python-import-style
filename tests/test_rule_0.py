# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._check_rule_0."""

import pathlib
import typing

import pytest
import test_utils

import python_import_style
import python_import_style._prepare_file_context
import python_import_style._rule_0


def _run_rule_0_for_file(
    package_name: str,
    _project_root: pathlib.Path,
    package_root: pathlib.Path,
    tests_root: pathlib.Path,
    file_paths: list[pathlib.Path],
) -> list[str]:
    """Run rule 0 for a file and return the list of error messages."""
    assert len(file_paths) == 1
    file_path = file_paths[0]

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


@pytest.mark.parametrize(
    "run_rule", [_run_rule_0_for_file, python_import_style.check_all_rules]
)
def test_rule_0_forbids_double_leading_underscore_in_module(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
) -> None:
    """Reject private module filenames that start with two underscores."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "__mod.py"
    mod.write_text("import os\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(errors, [(0, "private module name", 1)])


@pytest.mark.parametrize(
    "run_rule", [_run_rule_0_for_file, python_import_style.check_all_rules]
)
def test_rule_0_forbids_double_leading_underscore_in_subpackage(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
) -> None:
    """Reject subpackage directory names starting with two underscores."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "__subpkg" / "_mod.py"
    mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(errors, [(0, "private subpackage name", 1)])


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_0_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
@pytest.mark.parametrize("in_tests", [True, False])
def test_rule_0_allows_double_leading_underscore_outside_of_package(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
    in_tests: bool,
) -> None:
    """Allow double leading underscore outside of package.

    It does not make much sense to have a double leading underscore even
    outside of the package anyways, but rule 0 does not enforce this.
    """
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    if in_tests:
        mod = tests_root / "__subpkg" / "__mod.py"
    else:
        mod = tmp_path / "another_directory" / "__subpkg" / "__mod.py"
    mod.parent.mkdir(parents=True)
    mod.write_text("import os\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    assert len(errors) == 0
