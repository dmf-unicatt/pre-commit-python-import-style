# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Some utility functions for testing."""

import pathlib


def _initialize_package_and_tests_dirs(
    tmp_path: pathlib.Path,
) -> tuple[str, pathlib.Path, pathlib.Path]:
    """Initialize the package and tests directories for testing."""
    package_name = "my_package"
    package_root = tmp_path / package_name
    package_root.mkdir()
    tests_root = tmp_path / "tests"
    tests_root.mkdir()
    return package_name, package_root, tests_root


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
