# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Some utility functions for testing."""

import contextlib
import io
import os
import pathlib
import runpy
import subprocess
import sys

import pytest


def _initialize_package_and_tests_dirs(
    project_root: pathlib.Path,
) -> tuple[str, pathlib.Path, pathlib.Path]:
    """Initialize the package and tests directories for testing."""
    package_name = "my_package"
    package_root = project_root / package_name
    package_root.mkdir()
    tests_root = project_root / "tests"
    tests_root.mkdir()
    subprocess.run(
        ["git", "init"],
        cwd=str(project_root),
        check=True,
    )
    return package_name, package_root, tests_root


def _run_cli_and_get_errors(
    package_name: str,
    project_root: pathlib.Path,
    package_root: pathlib.Path,
    tests_root: pathlib.Path,
    file_paths: list[pathlib.Path],
) -> list[str]:
    """Run the CLI on the given files and return the list of error messages."""
    old_argv = sys.argv[:]
    old_cwd = pathlib.Path.cwd()
    stdout_buffer = io.StringIO()

    try:
        sys.argv[:] = [
            "python_import_style",
            "--root-dir",
            project_root.as_posix(),
            "--package-dir-prefix",
            package_root.relative_to(project_root).parent.as_posix(),
            "--package-name",
            package_name,
            "--tests-dir",
            tests_root.relative_to(project_root).as_posix(),
            *[str(file.relative_to(project_root)) for file in file_paths],
        ]
        os.chdir(project_root)
        with contextlib.redirect_stdout(stdout_buffer):
            with pytest.raises(SystemExit) as exc:
                runpy.run_module(
                    "python_import_style", run_name="__main__", alter_sys=True
                )
            if exc.value.code == 0:
                return []
            else:
                return stdout_buffer.getvalue().strip().split("\n")
    finally:
        sys.argv[:] = old_argv
        os.chdir(old_cwd)


def _assert_rule_errors(
    errors: list[str],
    expected_errors: list[tuple[int, str, int]],
) -> None:
    """Return True if any error message contains the given rule number."""
    total_actual_occurences = 0
    for rule_number, text, expected_occurences in expected_errors:
        actual_occurences = sum(
            f"Rule {rule_number}" in error and text in error for error in errors
        )
        assert actual_occurences == expected_occurences, (
            f"Expected {expected_occurences} "
            f"occurrences of Rule {rule_number} with text '{text}' in "
            f"errors, but found {actual_occurences}. "
            f"The full error list was:\n" + "\n".join(errors)
        )
        total_actual_occurences += actual_occurences

    assert total_actual_occurences == len(errors), (
        f"Expected {len(errors)} errors, but found {total_actual_occurences}. "
        f"The full error list was:\n" + "\n".join(errors)
    )
