# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._check_rule_2."""

import pathlib
import typing

import pytest
import test_utils

import python_import_style
import python_import_style._get_tree_from_file
import python_import_style._rule_2


def _run_rule_2_for_file(
    _package_name: str,
    _project_root: pathlib.Path,
    _package_root: pathlib.Path,
    _tests_root: pathlib.Path,
    file_paths: list[pathlib.Path],
) -> list[str]:
    """Run rule 2 for a file and return the list of error messages."""
    assert len(file_paths) == 1
    file_path = file_paths[0]

    tree, _ = python_import_style._get_tree_from_file._get_tree_from_file(
        file_path
    )
    assert tree is not None

    return python_import_style._rule_2._rule_2(
        file_path,
        tree,
    )


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_2_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
@pytest.mark.parametrize("directory_name", ["my_package", "tests", "outside"])
def test_rule_2_forbids_from_import_aliases(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
    directory_name: str,
) -> None:
    """Flag disallowed from import aliases."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = tmp_path / directory_name / "mod.py"
    mod.parent.mkdir(exist_ok=True)
    mod.write_text("from os import path as os_path\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    expected_errors = [
        (2, "from ... import ... aliases are forbidden", 1),
    ]
    if run_rule != _run_rule_2_for_file:
        expected_errors.append(
            (1, "use 'import ...' instead of 'from ... import ...'", 1)
        )
    test_utils._assert_rule_errors(
        errors,
        expected_errors,
    )


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_2_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
@pytest.mark.parametrize("directory_name", ["my_package", "tests", "outside"])
def test_rule_2_forbids_import_aliases(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
    directory_name: str,
) -> None:
    """Flag disallowed import aliases."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = tmp_path / directory_name / "mod.py"
    mod.parent.mkdir(exist_ok=True)
    mod.write_text("import requests as rq\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(
        errors,
        [
            (2, "import aliases are forbidden, except for", 1),
        ],
    )


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_2_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
@pytest.mark.parametrize("directory_name", ["my_package", "tests", "outside"])
def test_rule_2_allows_curated_import_aliases(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
    directory_name: str,
) -> None:
    """Permit curated import aliases like `numpy as np` and `pandas as pd`."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = tmp_path / directory_name / "mod.py"
    mod.parent.mkdir(exist_ok=True)
    mod.write_text("import numpy as np\n", encoding="utf-8")

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(errors, [])
