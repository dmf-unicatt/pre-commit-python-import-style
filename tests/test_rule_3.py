# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._check_rule_3."""

import pathlib
import typing

import pytest
import test_utils

import python_import_style
import python_import_style._get_tree_from_file
import python_import_style._prepare_file_context
import python_import_style._rule_3


def _run_rule_3_for_file(
    package_name: str,
    _project_root: pathlib.Path,
    package_root: pathlib.Path,
    tests_root: pathlib.Path,
    file_paths: list[pathlib.Path],
) -> list[str]:
    """Run rule 3 for a file and return the list of error messages."""
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

    return python_import_style._rule_3._rule_3(
        file_path,
        file_context,
        tree,
    )


@pytest.mark.parametrize(
    "run_rule",
    [
        _run_rule_3_for_file,
        python_import_style.check_all_rules,
        test_utils._run_cli_and_get_errors,
    ],
)
@pytest.mark.parametrize(
    "module_name", ["mod.py", "_mod.py", "__init__.py", "__main__.py"]
)
@pytest.mark.parametrize(
    "relative_import_level", [".", "..", ".module", "..module.submodule"]
)
def test_rule_3_forbids_relative_imports_inside_package(
    tmp_path: pathlib.Path,
    run_rule: typing.Callable[
        [str, pathlib.Path, pathlib.Path, pathlib.Path, list[pathlib.Path]],
        list[str],
    ],
    module_name: str,
    relative_import_level: str,
) -> None:
    """Forbid relative imports in package modules."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    if ".." in relative_import_level:
        mod = package_root / "subpkg" / module_name
    else:
        mod = package_root / module_name
    mod.parent.mkdir(exist_ok=True)
    mod.write_text(
        f"from {relative_import_level} import something\n", encoding="utf-8"
    )

    errors = run_rule(package_name, tmp_path, package_root, tests_root, [mod])
    test_utils._assert_rule_errors(
        errors,
        [
            (
                3,
                "relative imports are forbidden inside the package",
                1,
            )
        ],
    )
