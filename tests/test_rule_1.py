# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._check_rule_1."""

import pathlib
import typing

import pytest
import test_utils

import python_import_style
import python_import_style._get_tree_from_file
import python_import_style._prepare_file_context
import python_import_style._rule_1


def _run_rule_1_for_file(
    package_name: str,
    _project_root: pathlib.Path,
    package_root: pathlib.Path,
    tests_root: pathlib.Path,
    file_paths: list[pathlib.Path],
) -> list[str]:
    """Run rule 1 for a file and return the list of error messages."""
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

    tree, _ = python_import_style._get_tree_from_file._get_tree_from_file(
        file_path
    )
    assert tree is not None

    return python_import_style._rule_1._rule_1(
        package_name,
        file_path,
        file_context,
        tree,
    )


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_1_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
@pytest.mark.parametrize("directory_name", ["my_package", "tests", "outside"])
def test_rule_1_forbids_from_import_outside_init(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
    directory_name: str,
) -> None:
    """Ensure `from ... import ...` is forbidden outside __init__.py."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = tmp_path / directory_name / "mod.py"
    mod.parent.mkdir(exist_ok=True)
    mod.write_text("from os import path\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(
        errors, [(1, "use 'import ...' instead of 'from ... import ...'", 1)]
    )


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_1_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
def test_rule_1_allows_from_import_in_init_for_private_module(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
) -> None:
    """Allow `from my_package import ...` in package `__init__` for exports."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "__init__.py"
    mod.write_text(
        "from my_package._internal import PublicName\n", encoding="utf-8"
    )

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(errors, [])


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_1_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
def test_rule_1_forbids_from_import_star_inside_init(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
) -> None:
    """Ensure `from my_package import *` is forbidden in __init__.py."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "__init__.py"
    mod.write_text("from my_package import *\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(
        errors,
        [
            (
                1,
                "wildcard imports (from ... import *) are not allowed",
                1,
            )
        ],
    )


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_1_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
def test_rule_1_forbids_non_package_from_import_inside_init(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
) -> None:
    """Ensure `from non_my_package import ...` is forbidden in __init__.py."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "__init__.py"
    mod.write_text("from os import path\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(
        errors,
        [
            (
                1,
                "in __init__.py, only use the syntax 'from ... import ...'",
                1,
            )
        ],
    )
